<template>
    <div class="Conjugations">
        <ReportModal :item="reportItem" @closeModal="setReportItem(null)"></ReportModal>
        <Conjugation
            v-for="form in response.forms"
            @reportClicked="setReportItem"
            :word="form.word"
            :group="form.group"
            :wordType="form.word_type"
            :pos="form.pos"></Conjugation>
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

    setReportItem(item) {
        this.reportItem = item;
    }
}
</script>
