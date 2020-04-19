<template>
    <div class="columns">
        <div class="column is-10">
            <input
                class="input"
                type="text"
                placeholder="Enter a word.."
                v-model="searchTerm"
                @keydown.enter="onSearch"
                />
        </div>
        <div class="column has-text-right">
            <button
                    class="button"
                    style="width: 100%;"
                    @click="onSearch">
                <span class="icon is-small">
                    <i class="fas fa-search"></i>
                </span>
                <span>Search</span>
            </button>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import { Component } from "vue-property-decorator";

@Component()
export default class SearchBox extends Vue {
    searchTerm: string | null = null;

    onSearch() {
        this.$emit("search", this.searchTerm);
    }
}
</script>

