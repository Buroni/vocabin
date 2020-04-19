<template>
    <div class="box">
        <SearchBox @search="onSearch"></SearchBox>
        <ButtonTray
            @optionsChange="onOptionsChange"
        >
        </ButtonTray>
    </div>
</template>
<script>
import Vue from "vue";
import ButtonTray from "../search-options/ButtonTray/ButtonTray";
import SearchBox from "../search-options/SearchBox/SearchBox";
import "reflect-metadata";
import { Component } from "vue-property-decorator";

const components = { ButtonTray, SearchBox };

@Component({ components })
export default class FloatingSearch extends Vue {
    onSearch(val) {
        this.$emit("search", val);
    }

    onOptionsChange(options) {
        this.$emit("optionsChange", options);
    }
}
</script>
