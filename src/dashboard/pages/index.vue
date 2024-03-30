<script setup lang="ts">
// Specify the layout we could have set a default layout but this is more explicit
definePageMeta({
    title: 'Dashboard',
    description: 'Dashboard page',
    layout: 'dashboard',
});

interface Location {
    id: number;
    name: string;
    latitude: Float32Array;
    longitude: Float32Array;
    weather?: any;
}

const openSidebar: Ref<any> = ref(false);
const sidebarData: Ref<any> = ref({});
// we need to use a ref to force the sidebar to re-render
let i = ref(0);
const handleOpenSidebar = (location: Location) => {
    i.value++;
    openSidebar.value = true;
    sidebarData.value = location;
};
</script>

<template>
    <!-- TODO Documentation and comments -->
    <!-- TODO maybe revise the backend and maybe getting current and daily differently would improve the performance -->
    <!-- TODO possibly add hourly weather -->
    <!-- TODO add unique identifier for multiple usage -->
    <Modal />
    <Table :openSidebar="handleOpenSidebar" />
    <Sidebar :key="i" :openSidebar="openSidebar" :data="sidebarData" />
    <UModals />
    <UNotifications />
</template>
