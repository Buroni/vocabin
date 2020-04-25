<style>
  @import './Conjugations.scss';
</style>

<template>
    <div class="Conjugations">
        <ReportModal :item="reportItem" @closeModal="setReportItem(null)"></ReportModal>
        <div class="box less-padding group" style="border: 0;">
        <div class="group-head">
            <i class="fas fa-equals" style="color: #3273dc;"></i>
            <div style="padding-left: 0.5em;">Exact Match</div>
        </div>
        <Conjugation
            @reportClicked="setReportItem"
            :form="userSearchForm"
            :noBorder="true"
        >
        </Conjugation>
        </div>
        <div
            v-if="!inflectionError"
            class="box group"
            style="margin-top: 2em; border: 0; padding-left: 0; padding-right: 0;"
            >
            <div class="group-head">
                <i class="fas fa-language" style="color: #3273dc;"></i>
                <div v-html="groupName(userSearchForm.group)" style="padding-left: 0.5em;"></div>
                <div class="group-head-meta">
                    <div><span v-html="relevantForms.length"></span> results</div>
                </div>
            </div>
            <div v-for="form in relevantForms">
                <div v-if="form.results.length === 1">
                    <Conjugation
                        v-for="(result, idx) in form.results"
                        @reportClicked="setReportItem"
                        :form="result"
                        :noBorder="idx === relevantForms.length - 1"
                        >
                    </Conjugation>
                </div>
                <div v-else>
                    <div>
                        <div v-html="specificWordType(form.word_type)" class="specific-word-type"></div>
                        <Conjugation
                            v-for="(result, idx) in form.results"
                            @reportClicked="setReportItem"
                            :form="result"
                            :noBorder="idx === relevantForms.length - 1"
                            >
                        </Conjugation>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="notification is-light" style="display: flex; align-items: center; border: 1px solid rgba(255, 0, 0, 0.7);">
          <div style="padding-right: 0.5em;"><i class="fas fa-bug" style="width: 1.4em; height: 1.4em; color: red; opacity: 0.7;"></i></div>
          <div>Sorry, an error occurred while trying to inflect this word. Hopefully the exact match is enough for now.</div>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import Caret from "../Caret/Caret";
import { Component, Prop } from "vue-property-decorator";
import Conjugation from "../Conjugation/Conjugation";
import ReportModal from "../ReportModal/ReportModal";
import { specificWordType } from "./utils";

const components = {
    Caret,
    Conjugation,
    ReportModal,
};

@Component({ components })
export default class Conjugations extends Vue {
    @Prop() response: any;

    reportItem: any | null = null;

    groupName(groupId: string): string {
        switch(groupId) {
            case "verb":
                return "Verb Forms";
            case "noun":
                return "Noun Forms";
            case "misc":
                return "Miscellaneous";
            default:
                return "Unknown";
        }
    }

    specificWordType(wordType: string): string {
        return specificWordType(wordType);
    }

    get userSearchForm() {
        return this.response.search_term;
    }

    get inflectionError(): boolean {
        return this.response.forms.length === 1 && this.groupId === "unk";
    }

    get relevantForms() {
        return this.response.forms.filter(form => {
            return form.group === this.userSearchForm.group;
        });
    }

    setReportItem(item) {
        this.reportItem = item;
    }
}
</script>
