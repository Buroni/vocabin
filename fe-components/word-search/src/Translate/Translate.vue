<style>
  @import './Translate.scss';
</style>

<template>
    <div class="Translate">
        <div v-if="errorMessage">
            <span v-html="errorMessage"></span>
            <span v-if="tryAgainText" class='fake-link' v-else @click='translate()'>Try again</span></span>
        </div>
        <div class="see-translation" v-else-if="loading">Translating..</div>
        <div class="translation" v-else-if="translation" v-html="translation"></div>
        <div class="see-translation" v-else style="display: flex; justify-content: flex-start; align-items: center;">
            <div class="fake-link" @click="translate()">See translation </div>
            <div class="select is-small" style="padding-left: 0.5em;">
                <select v-model="targetLang">
                    <option value="nl">to Dutch</option>
                    <option value="en">to English</option>
                    <option value="fr">to French</option>
                    <option value="de">to German</option>
                    <option value="it">to Italian</option>
                    <option value="es">to Spanish</option>
                </select>
            </div>
        </div>
    </div>
</template>

<script>
import { posTagToReadable } from "../utils";
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";
import vocaAPI from "../api";

@Component()
export default class Conjugation extends Vue {
    loading = false;
    translation: string | null = null;
    errorMessage: string | null = null;
    targetLang: string = "en";

    @Prop() sentence: string;

    async translate() {
        this.loading = true;
        this.tryAgainText = false;
        this.translation = null;
        this.errorMessage = null;
        try {
            const res = await vocaAPI.post("translate/", {"sentence": this.sentence, "target_lang": this.targetLang});
            this.translation = res.data["translation"];
        } catch(e) {
            this.handleErr(e);
        } finally {
            this.loading = false;
        }
    }

     handleErr(e) {
        if (e.message.includes("429")) {
            this.errorMessage = "<span class='see-translation'><i class='fas fa-info-circle'></i> Sorry, the translation feature is limited to 5 requests per minute!";
            this.tryAgainText = true;
        } else {
             this.errorMessage = e.message;
        }
    }
}
</script>
