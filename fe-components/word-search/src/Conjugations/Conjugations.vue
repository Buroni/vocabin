<template>
    <div class="Conjugations">
        <ReportModal :item="reportItem" @closeModal="setReportItem(null)"></ReportModal>
        <Conjugation
            @reportClicked="setReportItem"
            :form="userSearchForm">
        </Conjugation>
        <div v-for="groupName in Object.keys(groups)">
            <div v-html="groupName"></div>
            <Conjugation
                v-for="form in groups[groupName]"
                @reportClicked="setReportItem"
                :form="form">
            </Conjugation>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";
import Conjugation from "../Conjugation/Conjugation";
import ReportModal from "../ReportModal/ReportModal";

const components = {
    Conjugation,
    ReportModal
};

@Component({ components })
export default class Conjugations extends Vue {
    @Prop() response: any;

    reportItem: any | null = null;

    get userSearchForm() {
        return this.response.forms[0];
    }

    get groups() {
        const groups = {};
        this.response.forms.forEach(form => {
            const groupNames = Object.keys(groups);
            if (!groupNames.includes(form.group)) {
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
