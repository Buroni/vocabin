<template>
    <div class="box">
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
        <ButtonTray
            @optionsChange="onOptionsChange"
        >
        </ButtonTray>
    </div>
</template>
<script>
import Vue from "vue";
import ButtonTray from "../search-options/ButtonTray/ButtonTray";
import "reflect-metadata";
import { Component } from "vue-property-decorator";

const components = { ButtonTray };

@Component({ components })
export default class FloatingSearch extends Vue {
    searchTerm: string | null = null;

    onSearch() {
        this.$emit("search", this.searchTerm);
    }

    onOptionsChange(options) {
        // TODO -- better way than "emission drilling" to pass the message up?
        this.$emit("optionsChange", options);
    }
}
</script>
