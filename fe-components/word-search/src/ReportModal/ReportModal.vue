<style>
  @import './ReportModal.scss';
</style>

<template>
    <div class="ReportModal modal" :class="activeClass" v-if="item">
        <div class="modal-background" @click="closeModal"></div>
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Report Sentence</p>
            </header>
            <section class="modal-card-body" v-if="!submitted">
                <p class="sentence">
                    <i>{{ item.sentence }}</i>
                </p>
                <p>
                  Please report this sentence if
                  <div class="ol-container">
                      <ul>
                        <li>It's grammatically incorrect.</li>
                        <li>It's not a real sentence (e.g. a URL, number, random text).</li>
                        <li>It has discriminatory language -- including racism, homophobia, sexism.</li>
                      </ul>
                  </div>
                 </p>
            </section>
            <section class="modal-card-body" v-if="submitted">
                Thank you! Your report has been received.
            </section>
            <footer class="modal-card-foot" v-if="!submitted">
              <button class="button is-danger" @click="postReport">Report</button>
              <button class="button" @click="closeModal">Cancel</button>
            </footer>
            <footer class="modal-card-foot" v-if="submitted">
                <button class="button" @click="closeModal">Close</button>
            </footer>
        </div>
    </div>
</template>

<script>
import vocaAPI from "../api";
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";

@Component()
export default class ReportModal extends Vue {
    submitted = false;

    @Prop() item: any
    @Prop() close: any

    get activeClass() {
        return this.item ? "is-active" : "";
    }

    closeModal() {
        this.submitted = false;
        this.$emit("closeModal")
    }

    postReport() {
        vocaAPI.post("report/", { id: this.item.id });
        this.submitted = true;
    }
}
</script>
