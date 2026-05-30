<script lang="ts">
	import type { Collection, Category } from '$lib/types';
	import { t } from 'svelte-i18n';
	import FilterIcon from '~icons/mdi/filter-variant';
	import TagIcon from '~icons/mdi/tag-outline';
	import FolderIcon from '~icons/mdi/folder-outline';
	import SearchIcon from '~icons/mdi/magnify';
	import CloseIcon from '~icons/mdi/close';
	import ChevronDown from '~icons/mdi/chevron-down';
	import ChevronUp from '~icons/mdi/chevron-up';

	export let collection: Collection;
	export let search: string = '';
	export let selectedCategoryIds: string[] = [];
	export let selectedTags: string[] = [];
	export let matchCount: number | null = null;
	export let totalCount: number | null = null;

	let expanded = true;

	type CategoryOption = { id: string; display_name: string; icon: string; count: number };

	$: categoryOptions = (() => {
		const seen = new Map<string, CategoryOption>();
		for (const loc of collection?.locations ?? []) {
			const c = loc.category as Category | null | undefined;
			if (c && c.id) {
				const existing = seen.get(c.id);
				if (existing) {
					existing.count += 1;
				} else {
					seen.set(c.id, {
						id: c.id,
						display_name: c.display_name || c.name,
						icon: c.icon || '🏷️',
						count: 1
					});
				}
			}
		}
		return Array.from(seen.values()).sort((a, b) =>
			a.display_name.localeCompare(b.display_name)
		);
	})();

	$: tagOptions = (() => {
		const counts = new Map<string, number>();
		for (const loc of collection?.locations ?? []) {
			for (const tag of loc.tags ?? []) {
				if (tag) counts.set(tag, (counts.get(tag) ?? 0) + 1);
			}
		}
		return Array.from(counts.entries())
			.map(([tag, count]) => ({ tag, count }))
			.sort((a, b) => a.tag.localeCompare(b.tag));
	})();

	$: activeCount =
		((search ?? '').trim() ? 1 : 0) + selectedCategoryIds.length + selectedTags.length;
	$: hasActiveFilter = activeCount > 0;
	$: hasOptions = categoryOptions.length > 0 || tagOptions.length > 0;

	function toggleCategory(id: string) {
		selectedCategoryIds = selectedCategoryIds.includes(id)
			? selectedCategoryIds.filter((x) => x !== id)
			: [...selectedCategoryIds, id];
	}

	function toggleTag(tag: string) {
		selectedTags = selectedTags.includes(tag)
			? selectedTags.filter((x) => x !== tag)
			: [...selectedTags, tag];
	}

	function clearAll() {
		search = '';
		selectedCategoryIds = [];
		selectedTags = [];
	}
</script>

{#if hasOptions || hasActiveFilter}
	<div
		class="rounded-2xl border border-base-300/70 bg-base-100/80 backdrop-blur shadow-sm overflow-hidden"
	>
		<!-- Header -->
		<button
			type="button"
			class="w-full flex items-center gap-3 px-4 py-3 hover:bg-base-200/60 transition-colors"
			on:click={() => (expanded = !expanded)}
			aria-expanded={expanded}
		>
			<div class="flex items-center gap-2 text-base-content/80">
				<FilterIcon class="w-5 h-5" aria-hidden="true" />
				<span class="font-semibold">{$t('adventures.filter')}</span>
			</div>

			{#if hasActiveFilter}
				<span class="badge badge-primary badge-sm font-semibold">
					{activeCount}
				</span>
			{/if}

			<div class="flex-1" />

			{#if matchCount !== null && totalCount !== null && hasActiveFilter}
				<span class="text-sm text-base-content/60 mr-2 hidden sm:inline">
					{matchCount} / {totalCount} {$t('locations.locations')}
				</span>
			{/if}

			{#if hasActiveFilter}
				<button
					type="button"
					class="btn btn-ghost btn-xs gap-1 mr-1"
					on:click|stopPropagation={clearAll}
					aria-label={$t('adventures.clear')}
				>
					<CloseIcon class="w-3.5 h-3.5" aria-hidden="true" />
					{$t('adventures.clear')}
				</button>
			{/if}

			<span class="text-base-content/50">
				{#if expanded}
					<ChevronUp class="w-5 h-5" aria-hidden="true" />
				{:else}
					<ChevronDown class="w-5 h-5" aria-hidden="true" />
				{/if}
			</span>
		</button>

		{#if expanded}
			<div class="px-4 pb-4 pt-1 space-y-4 border-t border-base-300/50">
				<!-- Search input -->
				<label
					class="input input-bordered input-sm flex items-center gap-2 w-full focus-within:input-primary"
				>
					<SearchIcon class="w-4 h-4 opacity-60 shrink-0" aria-hidden="true" />
					<input
						type="text"
						class="grow bg-transparent outline-none"
						placeholder={$t('adventures.search')}
						bind:value={search}
					/>
					{#if (search ?? '').length > 0}
						<button
							type="button"
							class="btn btn-ghost btn-circle btn-xs"
							on:click={() => (search = '')}
							aria-label={$t('adventures.clear')}
						>
							<CloseIcon class="w-3.5 h-3.5" aria-hidden="true" />
						</button>
					{/if}
				</label>

				<!-- Categories -->
				{#if categoryOptions.length > 0}
					<div>
						<div class="flex items-center gap-2 mb-2 text-xs uppercase tracking-wide opacity-70">
							<FolderIcon class="w-3.5 h-3.5" aria-hidden="true" />
							<span>{$t('categories.categories')}</span>
						</div>
						<div class="flex flex-wrap gap-2">
							{#each categoryOptions as cat (cat.id)}
								{@const active = selectedCategoryIds.includes(cat.id)}
								<button
									type="button"
									class="group inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-all
										{active
										? 'border-primary bg-primary text-primary-content shadow-sm'
										: 'border-base-300 bg-base-100 hover:border-primary/60 hover:bg-base-200'}"
									on:click={() => toggleCategory(cat.id)}
									aria-pressed={active}
								>
									<span aria-hidden="true">{cat.icon}</span>
									<span>{cat.display_name}</span>
									<span
										class="text-xs opacity-60
											{active ? 'text-primary-content/80' : ''}"
									>
										{cat.count}
									</span>
								</button>
							{/each}
						</div>
					</div>
				{/if}

				<!-- Tags -->
				{#if tagOptions.length > 0}
					<div>
						<div class="flex items-center gap-2 mb-2 text-xs uppercase tracking-wide opacity-70">
							<TagIcon class="w-3.5 h-3.5" aria-hidden="true" />
							<span>{$t('adventures.tags')}</span>
						</div>
						<div class="flex flex-wrap gap-2">
							{#each tagOptions as { tag, count } (tag)}
								{@const active = selectedTags.includes(tag)}
								<button
									type="button"
									class="group inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-all
										{active
										? 'border-secondary bg-secondary text-secondary-content shadow-sm'
										: 'border-base-300 bg-base-100 hover:border-secondary/60 hover:bg-base-200'}"
									on:click={() => toggleTag(tag)}
									aria-pressed={active}
								>
									<TagIcon class="w-3 h-3" aria-hidden="true" />
									<span>{tag}</span>
									<span
										class="text-xs opacity-60
											{active ? 'text-secondary-content/80' : ''}"
									>
										{count}
									</span>
								</button>
							{/each}
						</div>
					</div>
				{/if}

				{#if !hasOptions}
					<p class="text-sm text-base-content/60 italic">
						{$t('adventures.no_location_types_match') ?? 'No categories or tags on locations yet.'}
					</p>
				{/if}
			</div>
		{/if}
	</div>
{/if}
