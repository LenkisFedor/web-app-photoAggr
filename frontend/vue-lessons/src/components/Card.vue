<script setup>
import { ref, computed } from 'vue';

import SelectedCard from './SelectedCard.vue';

const props = defineProps({
  imageUrl: String,
  title: String,
  price: Number,
  isAdded: Boolean,
  onClickAdd: Function
});

const isSelected = ref(false);
const cardPosition = ref('aboslute')
const cardShadow = ref('0 0 #0000')
const zIndex = ref(0)

const toggleSelected = () => {
  isSelected.value = !isSelected.value;
};

const getImageUrl = (imageUrl) => {
  return '/' + imageUrl.replace('./', '');
};

const cardStyle = computed(() => {
  if (isSelected.value) {

    cardPosition.value = 'fixed'
    cardShadow.value = '0 25px 50px -12px rgb(0 0 0 / 0.25)'
    zIndex.value = 30
    return {
      position: cardPosition.value,
      width: '55%',
      boxShadow: cardShadow.value,
      transform: 'scale(1.2)',
      zIndex:zIndex.value,
      transition: 'transform 0.5s, width 0.5s 0.5s, box-shadow 0.5s'
    };
  } else {

    setTimeout(() => {
      cardPosition.value = 'relative';
      cardShadow.value = '0 0 #0000';
      zIndex.value = 0;
    }, 700);

    return {
      zIndex:zIndex.value
    };
  }
});
</script>

<template>
  <div 
    class="relative w-1/3 bg-white rounded-2xl p-5 cursor-pointer hover:z-10 transition-transform duration-300"
    :class="{ 
      'hover:-translate-y-2 hover:shadow-lg ': !isSelected, 
      'z-30': isSelected
    }"
    @click="toggleSelected"
    :style="cardStyle"
  > 
    <div class="flex flex-col"> 
      <div class="text-center">
        <img :src="getImageUrl(imageUrl)" alt="" class="size-48 mx-auto">
        <p class="capitalize">{{ title }}</p>
      </div>
      <div class="flex justify-between mt-5">
        <div class="flex flex-col">
          <span class="text-slate-400">Цена</span>
          <b>{{ price }} р.</b>
        </div>
      </div>
    </div>
  </div>
  <SelectedCard
   v-if="isSelected"
   :isSelected = "isSelected"
   :price = "price"
   :imageUrl = "getImageUrl(imageUrl)"
   ></SelectedCard>
</template>

