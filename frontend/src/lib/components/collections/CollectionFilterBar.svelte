<script lang="ts">
	import type { Collection, Category } from '$lib/types';
	import { t } from 'svelte-i18n';
	import Filter from '~icons/mdi/filter-variant';
	import Tag from '~icons/mdi/tag';
	import Folder from '~icons/mdi/folder';
	import Search from '~icons/mdi/magnify';
	import Close from '~icons/mdi/close';

	export let collection: Collection;
	export let search: string = '';
	export let selectedCategoryIds: Set<string> = new Set();
	export let selectedTags: Set<string> = new Set();

	type CategoryOption = { id: string; display_name: string; icon: string };

	$: categoryOptions = (() => {
		const seen = new Map<string, CategoryOption>();
		for (const loc of collection?.locations ?? []) {
			const c = loc.category as Category | null | undefined;
			if (c && c.id && !seen.has(c.id)) {
				seen.set(c.id, {
					id: c.id,
					display_name: c.display_name || c.name,
					icon: c.icon || '🏷️'
				});
			}
		}
		return Array.from(seen.values()).sort((a, b) =>
			a.display_name.localeCompare(b.display_name)
		);
	})();

	$: tagOptions = (() => {
		const seen = new Set<string>();
		for (const loc of collection?.locations ?? []) {
			for (const tag of loc.tags ?? []) {
				if (tag) seen.add(tag);
			}
		}
		return Array.from(seen).sort((a, b) => a.localeCompare(b));
	})();

	$: hasActiveFilter =
		(search ?? '').trim().length > 0 ||
		selectedCategoryIds.size > 0 ||
		selectedTags.size > 0;

	function toggleCategory(id: string) {
		const next = new Set(selectedCategoryIds);
		if (next.has(id)) next.delete(id);
		else next.add(id);
		selectedCategoryIds = next;
	}

	function toggleTag(tag: string) {
		const next = new Set(selectedTags);
		if (next.has(tag)) next.delete(tag);
		else next.add(tag);
		selectedTags = next;
	}

	function clearAll() {
		search = '';
		selectedCategoryIds = new Set();
		selectedTags = new Set();
	}
</script>

{#if categoryOptions.length > 0 || tagOptions.length > 0 || hasActiveFilter}
	<div class="card bg-base-200/60 border border-base-300/60 shadow-sm">
		<div class="card-body p-4 gap-3">
			<div class="flex items-center justify-between gap-2 flex-wrap">
				<div class="flex items-center gap-2 font-semibold">
					<Filter class="w-5 h-5" aria-hidden="true" />
					<span>{$t('adventures.filter') || 'Filter'}</span>
				</div>
				<label class="input input-sm input-bordered flex items-center gap-2 flex-1 min-w-[12rem] max-w-md">
					<Search class="w-4 h-4 opacity-60" aria-hidden="true" />
					<input
						type="text"
						class="grow"
						placeholder={$t('adventures.search') || 'Search locations…'}
						bind:value={search}
					/>
				</label>
				{#if hasActiveFilter}
					<button
						type="button"
						class="btn btn-sm btn-ghost gap-1"
						on:click={clearAll}
						aria-label="Clear filters"
					>
						<Close class="w-4 h-4" aria-hidden="true" />
						{$t('adventures.clear') || 'Clear'}
					</button>
				{/if}
			</div>

			{#if categoryOptions.length > 0}
				<div class="flex items-start gap-2 flex-wrap">
					<div class="flex items-center gap-1 text-sm opacity-70 shrink-0 mt-1">
						<Folder class="w-4 h-4" aria-hidden="true" />
						<span>{$t('categories.categories') || 'Categories'}</span>
					</div>
					<div class="flex flex-wrap gap-2">
						{#each categoryOptions as cat (cat.id)}
							<button
								type="button"
								class="badge badge-lg gap-1 cursor-pointer transition-colors {selectedCategoryIds.has(
									cat.id
								)
									? 'badge-primary'
									: 'badge-outline hover:badge-neutral'}"
								on:click={() => toggleCategory(cat.id)}
							>
								<span aria-hidden="true">{cat.icon}</span>
								<span>{cat.display_name}</span>
							</button>
						{/each}
					</div>
				</div>
			{/if}

			{#if tagOptions.length > 0}
				<div class="flex items-start gap-2 flex-wrap">
					<div class="flex items-center gap-1 text-sm opacity-70 shrink-0 mt-1">
						<Tag class="w-4 h-4" aria-hidden="true" />
						<span>{$t('adventures.tags') || 'Tags'}</span>
					</div>
					<div class="flex flex-wrap gap-2">
						{#each tagOptions as tag (tag)}
							<button
								type="button"
								class="badge badge-lg gap-1 cursor-pointer transition-colors {selectedTags.has(
									tag
								)
									? 'badge-secondary'
									: 'badge-outline hover:badge-neutral'}"
								on:click={() => toggleTag(tag)}
							>
								<Tag class="w-3 h-3" aria-hidden="true" />
								<span>{tag}</span>
							</button>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
