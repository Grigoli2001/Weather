<template>
    <div>
        <UContainer class="mt-4">
            <UTable
                :loading="pending"
                :empty-state="{ icon: 'i-heroicons-circle-stack-20-solid', label: 'No items.' }"
                :columns="columns"
                :rows="tableData"
                class="overflow-hidden tablecontainer"
                :ui="{
                    td: {
                        base: 'dark:bg-neutral-900 xl:last:w-[32rem] last:text-right bg-neutral-100',
                        padding: 'p-2 first:pl-4',
                    },
                    th: { base: 'dark:bg-customGray bg-neutral-200', padding: 'px-2 py-4 first:pl-4' },
                }"
            >
                <template #actions-data="{ row }">
                    <div class="w-full cursor-pointer" @click="handleOpenSidebar(row)">
                        <UButton
                            color="gray"
                            variant="ghost"
                            class="dark:text-zinc-500 mr-3"
                            :icon="action.icon"
                            @click="action.onClick($event, row)"
                        />
                    </div>
                </template>
                <template #name-data="{ row }">
                    <div class="w-full cursor-pointer" @click="handleOpenSidebar(row)">
                        <div class="flex align-middle items-center">
                            <img :src="'/_nuxt/assets/icons/' + getIcon(row.weatherCode)" alt="" />
                            <p class="ml-4 dark:text-blue-100 cursor-pointer dark:hover:text-blue-200 hover:underline">
                                {{ row.name }}
                            </p>
                        </div>
                    </div>
                </template>
                <template #temperature-data="{ row }">
                    <p @click="handleOpenSidebar(row)" class="cursor-pointer">{{ row.temperature }}</p>
                </template>
                <template #rainfall-data="{ row }">
                    <p @click="handleOpenSidebar(row)" class="cursor-pointer">{{ row.rainfall }}</p>
                </template>
            </UTable>
        </UContainer>

        <!-- Delete Confirmation Popup -->
        <UModal
            v-model="deleteModal"
            :overlay="false"
            :ui="{
                width: 'w-fit',
                container: 'items-start',
            }"
        >
            <UCard class="dark:bg-neutral-900">
                <h1 class="text-xl">Are you sure you want to remove {{ deleteRow?.name }}?</h1>
                <div class="flex justify-end mt-4">
                    <UButton color="gray" variant="ghost" label="Cancel" @click="deleteModal = false" class="mr-2" />
                    <UButton
                        color="red"
                        variant="solid"
                        label="Delete"
                        @click="deleteLocation(deleteRow.id, deleteRow.name)"
                    />
                </div>
            </UCard>
        </UModal>
    </div>
</template>

<script setup lang="ts">
interface Location {
    id: number;
    name: string;
    latitude: Float32Array;
    longitude: Float32Array;
    weather?: any;
}
const columns = [
    {
        key: 'name',
        label: 'Location',
    },
    {
        key: 'temperature',
        label: 'Temperature',
    },
    {
        key: 'rainfall',
        label: 'Rainfall',
    },
    {
        key: 'actions',
        label: '',
    },
];

const action = {
    icon: 'i-heroicons-trash',
    onClick: (event: any, row: any) => {
        event.stopPropagation();
        deleteModal.value = true;
        deleteRow.value = row;
    },
};

const deleteModal = ref(false);
const deleteRow: any = ref({});
const toast = useToast();
let tableData: any = ref([]);

const { data: locations, pending } = await useLazyAsyncData<Location[]>('locations', () =>
    $fetch('http://127.0.0.1:8000/locations/', {
        method: 'GET',
        onResponse: ({ response }) => {
            console.log(response);
            tableData = response._data?.map((location: any) => {
                return {
                    id: location.id,
                    name: location.name,
                    temperature: parseInt(location.weather?.current?.temperature_2m) + '°C',
                    rainfall: parseInt(location.weather?.current?.precipitation) + 'mm',
                    weatherCode: location.weather?.current?.weather_code,
                    daily: location.weather?.daily,
                };
            });
        },
    })
);

const deleteLocation = async (id: number, name: string) => {
    await $fetch(`http://127.0.0.1:8000/locations/${id}`, {
        method: 'DELETE',
        onResponse: ({ response }) => {
            if (response.status === 204) {
                toast.add({
                    title: 'Success',
                    description: `${name} has been deleted`,
                });
                refreshNuxtData('locations');
                deleteModal.value = false;
                deleteRow.value = {};
            }
        },
    });
};

// get props
const { openSidebar } = defineProps<{
    openSidebar: (row: any) => void;
}>();

// utils
const handleOpenSidebar = (row: any) => {
    openSidebar(row);
};
const getIcon = (weatherCode: number) => {
    if (weatherCode == 0 || weatherCode == 1) {
        return '1.svg';
    } else if (weatherCode == 2) {
        return '3.svg';
    } else if (weatherCode <= 50) {
        return '4.svg';
    } else if (
        weatherCode == 51 ||
        weatherCode == 53 ||
        weatherCode == 61 ||
        weatherCode == 63 ||
        weatherCode == 80 ||
        weatherCode == 81
    ) {
        return '5.svg';
    } else {
        return '2.svg';
    }
};
</script>
