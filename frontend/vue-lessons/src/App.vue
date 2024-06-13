<template>
  <!-- <Drawer></Drawer> -->
  <div class="bg-white w-4/5 m-auto rounded-3xl shadow-2xl mt-10 mb-20 pb-1">
    <Header></Header>
      <div class="p-3">
        <h2 class="text-3xl font-bold m-8"> Услуги </h2>
        <CardList items=""></CardList>
      </div>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import Header from './components/Header.vue'
import CardList from './components/CardList.vue'
import Drawer from './components/Drawer.vue'
</script>
