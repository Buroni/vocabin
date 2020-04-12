<style>
  @import './ErrorCard.scss';
</style>

<template>
    <div class="ErrorCard">
        <article class="message is-danger">
            <div class="message-header">
                <p>An error occurred</p>
            </div>
          <div class="message-body">
            {{ message }}
          </div>
        </article>
    </div>
</template>

<script>
import Vue from "vue";
import "reflect-metadata";
import { Component, Prop } from "vue-property-decorator";

@Component()
export default class ErrorCard extends Vue {
    @Prop() message: string;
}
</script>

