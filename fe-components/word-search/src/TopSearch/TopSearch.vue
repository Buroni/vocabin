<style>
  @import './TopSearch.scss';
</style>


<template>
    <div class="TopSearch">
        <div class="search-container">
            <div class="search-box">
                <input
                    class="input is-small search-box"
                    type="text"
                    placeholder="Enter a word.."
                    v-model="reactiveSearchTerm"
                    @keydown.enter="onSearch"
                />
            </div>
            <div class="tray-container">
                <ButtonTray @optionsChange="onOptionsChange" :small="true"></ButtonTray>
            </div>
            <div class="button-container">
                <button
                    class="button is-small"
                    @click="onSearch">
                    <span class="icon is-small">
                        <i class="fas fa-search"></i>
                    </span>
                    <span>Search</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import ButtonTray from "../search-options/ButtonTray/ButtonTray";
import SearchBox from "../search-options/SearchBox/SearchBox";
import "reflect-metadata";
import { Component, InjectReactive } from "vue-property-decorator";

const components = { ButtonTray, SearchBox };

@Component({ components })
export default class TopSearch extends Vue {
    @InjectReactive() searchTerm: string | null;

    reactiveSearchTerm: string | null = null;

    created() {
        this.reactiveSearchTerm = this.searchTerm;
    }

    onSearch() {
        this.$emit("search", this.reactiveSearchTerm);
    }

    onOptionsChange(options) {
        this.$emit("optionsChange", options);
    }
}
</script>
