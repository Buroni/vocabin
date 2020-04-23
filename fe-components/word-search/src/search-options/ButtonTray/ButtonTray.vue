<style>
  @import './ButtonTray.scss';
</style>

<template>
    <div class="ButtonTray">
        <div class="buttons-container" :class="sizeClass">
            <div class="select" :class="sizeClass">
                <select v-model="reactiveLang">
                    <option value="nl">Dutch</option>
                    <option value="en">English</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="it">Italian</option>
                    <option value="es">Spanish</option>
                </select>
            </div>
            <div class="select" :class="sizeClass">
                <select v-model="reactiveDifficulty">
                    <option value="">Any difficulty</option>
                    <option value="0">Simple results</option>
                </select>
            </div>
            <div class="select" :class="sizeClass">
                <select v-model="reactiveCategory">
                    <option value="">Any category</option>
                    <option value="news">News</option>
                    <option value="web">Web</option>
                </select>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import BaseSearch from "../BaseSearch/BaseSearch";
import "reflect-metadata";
import { Component, InjectReactive, Prop, Watch } from "vue-property-decorator";

@Component()
export default class ButtonTray extends Vue {
    @Prop() small: boolean;

    @InjectReactive() lang: string;
    @InjectReactive() difficulty: string;
    @InjectReactive() category: string;

    // App.vue injects properties to this component whose changes are then sent back via reactive*
    // TODO -- Maybe better to use a state management lib like mobx/redux
    reactiveLang: string = "";
    reactiveDifficulty = null;
    reactiveCategory = null;

    created() {
        this.reactiveLang = this.lang;
        this.reactiveDifficulty = this.difficulty;
        this.reactiveCategory = this.category;
    }

    get options() {
        return {
            lang: this.reactiveLang,
            difficulty: this.reactiveDifficulty,
            category: this.reactiveCategory,
        };
    }

    get sizeClass() {
        return this.small && "is-small";
    }

    // TODO - Create "WatchAll" decorator

    @Watch("reactiveLang")
    onLangChange(val) {
        this.$emit("optionsChange", this.options);
    }

    @Watch("reactiveDifficulty")
        onDifficultyChange(val) {
        this.$emit("optionsChange", this.options);
    }

    @Watch("reactiveCategory")
    onLangChange(val) {
        this.$emit("optionsChange", this.options);
    }
}
</script>
