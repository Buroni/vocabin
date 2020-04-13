<style>
  @import './App.scss';
</style>

<template>
    <div>
        <section class="section">
            <div class="App">
                <div class="box">
                    <div class="columns">
                        <div class="column is-10">
                            <input
                                class="input"
                                type="text"
                                placeholder="Enter a word.."
                                v-model="searchTerm"
                                @keydown.enter="get"
                                />
                        </div>
                        <div class="column has-text-right">
                            <button
                                    class="button"
                                    style="width: 100%;"
                                    @click="get">
                                <span class="icon is-small">
                                    <i class="fas fa-search"></i>
                                </span>
                                <span>Search</span>
                            </button>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div class="select">
                            <select v-model="lang">
                                <option value="en">English</option>
                                <option value="fr">French</option>
                                <option value="de">German</option>
                            </select>
                        </div>
                        <div class="select">
                            <select v-model="difficulty">
                                <option value="">Any difficulty</option>
                                <option value="0">Only simple results</option>
                            </select>
                        </div>
                        <div class="select">
                            <select v-model="category">
                                <option value="">Any category</option>
                                <option value="news">News</option>
                                <option value="web">Web</option>
                                <option value="kids" disabled>Kids (coming soon)</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section mid-section">
            <article class="message is-gray" v-if="!showSectionBox">
              <div class="message-body" style="border-color: #3273dc;">
                <p><b>Vocabin</b> is a language-learning tool which shows example sentences for each inflection of a given word.
                Sentences can be filtered by difficulty level and category. Enter a word above to try it out!</p>
              </div>
            </article>
            <div class="box" v-if="showSectionBox">
                <div v-if="errorMessage">
                    <ErrorCard :message="errorMessage"></ErrorCard>
                </div>
                <div v-if="loading && !errorMessage">
                    <p>
                    <i class="fas fa-list head-icon"></i>
                    Fetching results...
                    </p>
                </div>
                <div v-else-if="!loading && !noResults">
                    <Conjugations :response="response">
                </div>
                <div v-else-if="noResults">
                    No results found for "{{ response.forms[0] }}"!
                </div>
            </div>
        </section>

    </div>
</template>

<script>
import vocaAPI from "../api";
import Conjugations from "../Conjugations/Conjugations";
import ErrorCard from "../ErrorCard/ErrorCard";
import { noResults } from "../utils";
import Vue from "vue";
import "reflect-metadata";
import { Component, ProvideReactive } from "vue-property-decorator";

const components = {
    Conjugations,
    ErrorCard
};

@Component({ components })
export default class App extends Vue {

    response: any = null;
    loading = false;
    noResults = false;
    errorMessage: string | null = null;
    showTooltip = false;

    @ProvideReactive() searchTerm: string | null = null;
    @ProvideReactive() lang: string = "en";
    @ProvideReactive() difficulty: string = "";
    @ProvideReactive() category: string = "";

    get showSectionBox() {
        return this.response || this.noResults || this.loading;
    }

    /* Fetch sentences for a given search term (word) and store in this.response */
    async get() {
        this.loading = true;
        this.resetParams();
        try {
            const res = await vocaAPI.get(`forms/${this.lang}/${this.searchTerm}/`);
            if (res.data["forms"].length === 0) {
                this.noResults = true;
            }
            this.response = res.data;
            this.loading = false;
        } catch(e) {
            this.handleErr(e);
        }
    }

    handleErr(e) {
       this.errorMessage = e.message;
    }

    /* Set the search/response params back to initial state */
    resetParams() {
        this.noResults = false;
        this.errorMessage = null;
        this.response = null;
    }
}
</script>
