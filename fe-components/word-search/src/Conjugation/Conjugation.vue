<style>
  @import './Conjugation.scss';
</style>

<template>
    <div class="Conjugation">
        <div :class="noResults">
            <div class="fake-link" @click="toggle">
                <div class="columns">
                    <div class="column is-7">
                        <h1 class="title word-caret is-size-5">
                            <div>{{ word }}</div>
                            <Caret class="caret" :key="expanded" :expanded="expanded"></Caret>
                        </h1>
                    </div>
                    <div class="column is-3">
                        <span class="subtitle is-size-6">{{ wordType }}</span>
                    </div>
                    <div class="column">
                        <span class="subtitle is-size-6">{{ sentences.length }} results</span>
                    </div>
                </div>
            </div>
            <div v-if="expanded">
                <div v-for="item in sentences" class="sentence-item">
                    <div class="columns tag-columns">
                        <div class="column">
                            <div class="tags are-small">
                                <span class="tag">
                                    <span class="icon"><i :class="categoryIconClass(item.category)"></i></span>
                                    <span class="tag-text">{{ item.category }}</span>
                                </span>
                            </div>
                        </div>
                        <div class="column">
                            <span class="tag is-pulled-right report-button" @click="onReportClick(item)">
                                <span class="icon"><i class="fas fa-flag"></i></span>
                            </span>
                        </div>
                    </div>
                    <div v-html="highlightSentence(item.sentence)"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { posTagToReadable } from "../utils";
import Caret from "../Caret/Caret";
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";

const components = { Caret };

@Component({ components })
export default class Conjugation extends Vue {
    public expanded = false;

    @Prop() word: string;
    @Prop() sentences: any[];
    @Prop() pos: string;

    get wordType() {
        return posTagToReadable(this.pos);
    }

    get showHide() {
        return this.expanded ? "hide" : "show";
    }

    get noResults() {
         return this.sentences.length === 0 ? "no-results" : "";
     }

    onReportClick(item) {
        this.$emit("reportClicked", item);
    }

    toggle() {
        this.expanded = !this.expanded;
    }

    categoryIconClass(cat) {
        let icon;
        switch (cat) {
            case "news":
                icon = "newspaper";
                break;
            case "web":
                icon = "globe"
                break;
            default:
                icon = "shapes"
        }
        return `fas fa-${icon}`;
    }

    /* Make the focused word bold in the sentence */
    highlightSentence(sentence) {
        return sentence.replace(new RegExp(`\\b${this.word}\\b`), `<b>${this.word}</b>`);
    }
}
</script>
