<style>
  @import './WordTypeGroup.scss';
</style>

<template>
    <div class="WordTypeGroup">
        <div class="specific-word-type" @click="toggle">
            <div class="word-type-wrapper">
                <div class="cat-icon-wrapper"><i class="cat-icon fas fa-list"></i></div>
                <div class="type-text" v-html="specificWordType(form.word_type)"></div>
                <div class="num-results-wrapper">
                    <div class="num-results"><span v-html="form.results.length"></span> results</div>
                    <Caret class="caret" :key="expanded" :expanded="expanded"></Caret>
                </div>
            </div>
        </div>
        <Conjugation
            v-if="expanded"
            v-for="(result, idx) in form.results"
            @reportClicked="onReportClicked"
            :result="result"
            :noBorder="idx === form.results.length - 1"
            >
        </Conjugation>
    </div>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import Caret from "../Caret/Caret";
import { Component, Prop } from "vue-property-decorator";
import Conjugation from "../Conjugation/Conjugation";
import { specificWordType } from "./utils";

const components = { Caret, Conjugation }

@Component({ components })
export default class WordTypeGroup extends Vue {
    @Prop() form;

    expanded = false;

    specificWordType(wordType: string): string {
        return specificWordType(wordType);
    }

    onReportClicked(item) {
        this.$emit("reportClicked", item);
    }

    toggle() {
        this.expanded = !this.expanded;
    }
}
</script>
