<script>
import { defineComponent, ref, onMounted } from 'vue';
import axios from 'axios';
import Card from './Card.vue';

export default defineComponent({
  name: 'ServiceList',
  components: {
    Card
  },
  setup() {
    const services = ref([]);

    const fetchServices = async () => {
      try {
        const response = await axios.get('http://localhost:8000/services');
        services.value = response.data;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    const onClickAdd = () => {
      // Ваш код для обработки нажатия кнопки
      console.log('Added to cart');
    };

    onMounted(() => {
      fetchServices();
    });

    return {
      services,
      onClickAdd
    };
  }
});
</script>

<template>
  <div class="flex flex-wrap gap-20  justify-center" v-auto-animate>
    <Card
      v-for="service in services"
      :key="service._id"
      :imageUrl="service.image_url"
      :title="service.service_type"
      :price="service.price"
      :isAdded="false"
      :onClickAdd="onClickAdd"
    />
  </div>
</template>