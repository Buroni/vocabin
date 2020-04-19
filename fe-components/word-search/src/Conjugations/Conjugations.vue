<style>
  @import './Conjugations.scss';
</style>

<template>
    <div class="Conjugations">
        <ReportModal :item="reportItem" @closeModal="setReportItem(null)"></ReportModal>
        <div class="box is-shadowless less-padding group" style="border: 0;">
        <div class="group-head">
            <i class="fas fa-equals" style="color: #3273dc;"></i>
            <div style="padding-left: 0.5em;">Exact Match</div>
        </div>
        <Conjugation
            @reportClicked="setReportItem"
            :form="userSearchForm"
        >
        </Conjugation>
        </div>
        <div v-for="groupId in Object.keys(groups)" class="box is-shadowless group" style="margin-top: 2em; border: 0; padding-left: 0;">
            <div class="group-head">
                <i class="fas fa-language" style="color: #3273dc;"></i>
                <div v-html="groupName(groupId)" style="padding-left: 0.5em;"></div>
                <div class="group-head-meta">
                    <div><span v-html="groups[groupId].length"></span> results</div>
                </div>
            </div>
            <Conjugation
                v-for="form in groups[groupId]"
                @reportClicked="setReportItem"
                :form="form">
            </Conjugation>
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

    get userSearchForm() {
        return this.response.forms.find(f => f.word === this.response.search_term);
    }

    get groups() {
        const groups = {};
        this.response.forms.forEach(form => {
            const groupIds = Object.keys(groups);
            if (!groupIds.includes(form.group)) {
                groups[form.group] = [form];
            } else {
                groups[form.group].push(form);
            }
        });
        return groups;
    }

    setReportItem(item) {
        this.reportItem = item;
    }
}
</script>
