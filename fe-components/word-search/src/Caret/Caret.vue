<template>
    <span class="icon"><i :class="caretIcon"></i></span></a>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";

@Component()
export default class Caret extends Vue {
    @Prop() expanded: boolean;

    get caretIcon() {
        const icon = this.expanded ? "angle-down" : "angle-right";
        return `fas fa-${icon}`;
    }
};
</script>
