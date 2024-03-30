<template>
    <USlideover
        class="overflow-auto"
        v-model="isOpen"
        :ui="{ overlay: { background: 'bg-neutral-200/75 dark:bg-neutral-800/75' } }"
    >
        <UCard
            class="flex flex-col flex-1 dark:bg-zinc-900"
            :ui="{ body: { base: 'flex-1', padding: 'px-4 py-0 pd-5 sm:px-6' }, ring: '', divide: '' }"
        >
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-2xl font-semibold leading-6 text-gray-900 dark:text-white">{{ data?.name }}</h3>
                    <UButton
                        color="gray"
                        variant="ghost"
                        icon="i-heroicons-x-mark-20-solid"
                        class="-my-1 dark:bg-neutral-800 active:border-none"
                        @click="isOpen = false"
                        size="2xs"
                    />
                </div>
            </template>
            <div>
                <p class="text-sm text-neutral-400 mb-2">This week</p>
            </div>
            <div v-for="(date, index) in data?.daily?.time">
                <UCard class="flex-1 dark:bg-customGray mb-3 rounded-xl">
                    <div class="flex justify-between align-middle items-center">
                        <!-- left side -->
                        <div class="flex">
                            <img :src="'/_nuxt/assets/icons/' + getIcon(data.daily.weather_code[index])" alt="" />

                            <h1 class="ml-4 text-3xl font-medium">{{ getDayOfWeek(date) }}</h1>
                        </div>
                        <!-- right side  -->
                        <div class="w-20">
                            <div class="flex justify-between w-full">
                                <p class="dark:text-neutral-300 text-sm">Min.</p>
                                <p class="text-sm">
                                    {{ parseInt(data.daily.temperature_2m_min[index]) + '°C' }}
                                </p>
                            </div>
                            <div class="flex justify-between w-full">
                                <p class="dark:text-neutral-300 text-sm">Max.</p>
                                <p class="text-sm">
                                    {{ parseInt(data.daily.temperature_2m_max[index]) + '°C' }}
                                </p>
                            </div>
                        </div>
                    </div>
                </UCard>
            </div>
        </UCard>
    </USlideover>
</template>

<script setup lang="ts">
// create a new interface for the data
interface data {
    daily: any;
    daily_units: any;
    id: number;
    name: string;
    rainfall: string;
    temperature: string;
    weatherCode: number;
}

// define the props
const { openSidebar, data } = defineProps<{
    openSidebar: Ref<boolean>;
    data: Ref<data>;
}>();
console.log(data);

// define the reactive variables
const isOpen = ref(openSidebar);

// create util functions
const getDayOfWeek = (dateString: string): string => {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const date = new Date(dateString);
    const dayIndex = date.getDay();
    return daysOfWeek[dayIndex];
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
