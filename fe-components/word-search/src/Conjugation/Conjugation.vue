<style>
  @import './Conjugation.scss';
</style>

<template>
    <div class="Conjugation" :class="borderClass">
        <div>
            <div class="fake-link" @click="toggle">
                <div class="word-info">
                    <div>
                        <h1 class="word-caret subtitle is-size-6">
                            <div style="margin-left: 1em;">{{ word }}</div>
                            <Caret class="caret" :key="expanded" :expanded="expanded"></Caret>
                        </h1>
                    </div>
                    <div class="word-type">
                        <span class="subtitle">{{ wordType }}</span>
                    </div>
                </div>
            </div>
            <div v-if="expanded">
                <div class="padding-wrapper">
                    <div v-if="errorMessage" style="padding-top: 0.5em;">
                        <ErrorCard :message="errorMessage"></ErrorCard>
                    </div>
                    <div v-else-if="loading" style="padding-top: 0.5em; padding-bottom: 0.5em;">
                        <p>
                            <i class="fas fa-list head-icon"></i>
                            Fetching results...
                        </p>
                    </div>
                    <div v-else-if="noResults">
                        No results found for "{{ word }}"!
                    </div>
                </div>
                <div class="sentence-items">
                    <div v-if="!loading && !noResults" v-for="item in sentences" class="sentence-item">
                        <div class="tag-columns">
                            <div>
                                <div class="tags are-small">
                                    <span class="tag">
                                        <span class="icon"><i :class="categoryIconClass(item.category)"></i></span>
                                        <span class="tag-text">{{ item.category }}</span>
                                    </span>
                                </div>
                            </div>
                            <div class="report-col">
                                <span class="tag is-pulled-right report-button" @click="onReportClick(item)">
                                    <span class="icon"><i class="fas fa-flag"></i></span>
                                </span>
                            </div>
                        </div>
                        <div v-html="highlightSentence(item.sentence)"></div>
                        <div style="padding-top: 1.5em">
                            <Translate :sentence="item.sentence"></Translate>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Caret from "../Caret/Caret";
import ErrorCard from "../ErrorCard/ErrorCard";
import Translate from "../Translate/Translate";
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop, Inject, InjectReactive } from "vue-property-decorator";
import vocaAPI from "../api";
import { ResultsCache } from "./types";

const components = { Caret, ErrorCard, Translate };

@Component({ components })
export default class Conjugation extends Vue {
    expanded = false;
    loading = false;
    sentences: any[] = [];
    noResults = false;
    errorMessage: string | null = null;

    @Prop() result: any;
    @Prop() noBorder: boolean;

    @InjectReactive() searchTerm: string;
    @InjectReactive() lang: string;
    @InjectReactive() difficulty: string;
    @InjectReactive() category: string
    
    _cache: ResultsCache | null = null;

    cache(): any | null {
        if (!this._cache) return null;
        const {searchTerm, lang, difficulty, category} = this._cache.options;
        // Check cache isn't stale
        if (
            searchTerm !== this.searchTerm ||
            lang !== this.lang ||
            difficulty !== this.difficulty ||
            category !== this.category) {
            return null;
        }
        return {"data": {"sentences": this._cache.sentences}};
    }

    setCache() {
        this._cache = {
            options: {
                searchTerm: this.searchTerm,
                lang: this.lang,
                category: this.category,
                difficulty: this.difficulty
            },
            sentences: this.sentences
        }
    }

    get borderClass() {
        return !this.noBorder && "has-border";
    }

    get showHide() {
        return this.expanded ? "hide" : "show";
    }

    get word(): string {
        return this.result.word;
    }

    get group(): string {
        return this.result.group;
    }

    get wordType(): string {
        return this.result.word_type;
    }

    async get() {
        this.loading = true;
        this.noResults = false;
        const params = {
            difficulty: this.difficulty,
            category: this.category
        };
        try {
            const cache = this.cache();
            const res = cache || await vocaAPI.get(`sentences/${this.lang}/${this.word}/`, params);
            if (res.data["sentences"].length === 0) {
                this.noResults = true;
            }
            this.sentences = res.data["sentences"];
            this.loading = false;
            // Update cache if necessary
            if (!cache) {
                this.setCache();
            }
        } catch(e) {
            this.handleErr(e);
        }
    }

     handleErr(e) {
           this.errorMessage = e.message;
    }

    onReportClick(item) {
        this.$emit("reportClicked", item);
    }

    toggle() {
        this.expanded = !this.expanded;
        if (this.expanded) {
            this.get();
        }
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
