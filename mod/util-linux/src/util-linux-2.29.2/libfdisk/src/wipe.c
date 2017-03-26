#include "c.h"
#include "strutils.h"

#ifdef HAVE_LIBBLKID
# include <blkid.h>
#endif

#include "fdiskP.h"

struct fdisk_wipe {
	struct list_head	wipes;
	uint64_t		start;		/* sectors */
	uint64_t		size;		/* sectors */
};

static struct fdisk_wipe *fdisk_get_wipe_area(
			struct fdisk_context *cxt,
			uint64_t start,
			uint64_t size)
{
	struct list_head *p;

	if (cxt == NULL || list_empty(&cxt->wipes))
		return NULL;

	list_for_each(p, &cxt->wipes) {
		struct fdisk_wipe *wp = list_entry(p, struct fdisk_wipe, wipes);
		if (wp->start == start && wp->size == size)
			return wp;
	}
	return NULL;
}

void fdisk_free_wipe_areas(struct fdisk_context *cxt)
{
	while (!list_empty(&cxt->wipes)) {
		struct fdisk_wipe *wp = list_entry(cxt->wipes.next,
				                  struct fdisk_wipe, wipes);
		DBG(WIPE, ul_debugobj(wp, "free [start=%ju, size=%ju]",
				(uintmax_t) wp->start, (uintmax_t) wp->size));
		list_del(&wp->wipes);
		free(wp);
	}
}

int fdisk_has_wipe_area(struct fdisk_context *cxt,
			uint64_t start,
			uint64_t size)
{
	return fdisk_get_wipe_area(cxt, start, size) != NULL;
}

/* Add/remove new wiping area
 *
 * Returns: <0 on error, or old area setting (1: enabled, 0: disabled)
 */
int fdisk_set_wipe_area(struct fdisk_context *cxt,
			uint64_t start,
			uint64_t size,
			int enable)
{
	struct fdisk_wipe *wp;

	if (FDISK_IS_UNDEF(start) || FDISK_IS_UNDEF(size))
		return -EINVAL;

	wp = fdisk_get_wipe_area(cxt, start, size);

	/* disable */
	if (!enable) {
		if (wp) {
			DBG(WIPE, ul_debugobj(wp, "disable [start=%ju, size=%ju]",
						(uintmax_t) start, (uintmax_t) size));
			list_del(&wp->wipes);
			free(wp);
			return 1;
		}
		return 0;
	}

	/* enable */
	if (wp)
		return 1;	/* already enabled */

	wp = calloc(1, sizeof(*wp));
	if (!wp)
		return -ENOMEM;

	DBG(WIPE, ul_debugobj(wp, "enable [start=%ju, size=%ju]",
				(uintmax_t) start, (uintmax_t) size));

	INIT_LIST_HEAD(&wp->wipes);
	wp->start = start;
	wp->size = size;
	list_add_tail(&wp->wipes, &cxt->wipes);

	return 0;
}

int fdisk_do_wipe(struct fdisk_context *cxt)
{
#ifdef HAVE_LIBBLKID
	struct list_head *p;
	blkid_probe pr;
	int rc;

	assert(cxt);
	assert(cxt->dev_fd >= 0);

	if (list_empty(&cxt->wipes))
		return 0;

	pr = blkid_new_probe();
	if (!pr)
		return -ENOMEM;

	list_for_each(p, &cxt->wipes) {
		struct fdisk_wipe *wp = list_entry(p, struct fdisk_wipe, wipes);
		blkid_loff_t start = (blkid_loff_t) wp->start * cxt->sector_size,
			     size = (blkid_loff_t) wp->size * cxt->sector_size;

		DBG(WIPE, ul_debugobj(wp, "initialize libblkid prober [start=%ju, size=%ju]",
                                            (uintmax_t) start, (uintmax_t) size));

		rc = blkid_probe_set_device(pr, cxt->dev_fd, start, size);
		if (rc) {
			DBG(WIPE, ul_debugobj(wp, "blkid_probe_set_device() failed [rc=%d]", rc));
			return rc;
		}

		blkid_probe_enable_superblocks(pr, 1);
		blkid_probe_set_superblocks_flags(pr, BLKID_SUBLKS_MAGIC);
		blkid_probe_enable_partitions(pr, 1);
		blkid_probe_set_partitions_flags(pr, BLKID_PARTS_MAGIC);

		while (blkid_do_probe(pr) == 0) {
			DBG(WIPE, ul_debugobj(wp, " wiping..."));
			blkid_do_wipe(pr, FALSE);
		}
	}

	blkid_free_probe(pr);
#endif
	return 0;
}
