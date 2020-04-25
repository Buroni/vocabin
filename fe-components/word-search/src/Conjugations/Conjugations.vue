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
            :result="userSearchForm"
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
            </div>
            <Conjugation
                v-for="(form, idx) in singleResultForms"
                @reportClicked="setReportItem"
                :result="form.results[0]"
                :noBorder="idx === singleResultForms.length - 1"
                >
            </Conjugation>
            <WordTypeGroup
                v-for="form in multiResultForms"
                :form="form">
            </WordTypeGroup>
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
import WordTypeGroup from "../WordTypeGroup/WordTypeGroup";

const components = {
    Caret,
    Conjugation,
    ReportModal,
    WordTypeGroup,
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

    get userSearchForm() {
        return this.response.search_term;
    }

    get singleResultForms() {
        return this.relevantForms.filter(f => f.results.length === 1);
    }

    get multiResultForms() {
        return this.relevantForms.filter(f => f.results.length > 1);
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
