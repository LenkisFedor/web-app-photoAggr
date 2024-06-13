<template>
    <header class="flex justify-between border-b border-slate-100 px-10 py-10">
      <div class="flex items-center gap-4">
        <div>
          <h2 class="text-xl font-bold uppercase">@Vue Photo</h2>
          <p class="text-slate-500">Photo Aggregator</p>
        </div>
      </div>

      <ul class="flex items-center gap-10 text-gray-500">
        <li class="hover:text-black cursor-pointer">
          <span>Корзина</span>
        </li>
        <li class="hover:text-black cursor-pointer">
          <span>Закладки</span>
        </li>
        <li class="hover:text-black cursor-pointer">
          <span>Профиль</span>
        </li>
      </ul>
    </header>
</template>