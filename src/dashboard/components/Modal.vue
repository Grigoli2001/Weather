<template>
    <UContainer class="mt-14">
        <div class="flex justify-between align-middle">
            <h1 class="text-center text-3xl font-base">Locations</h1>
            <UButton
                icon="i-heroicons-plus-small-20-solid"
                variant="solid"
                label="Add Location"
                @click="isOpen = true"
                class="dark:bg-blue-100 dark:hover:bg-blue-200 font-bold text-sm px-3 py-1"
            />

            <UModal
                :ui="{
                    width: 'w-96',
                    overlay: { background: 'bg-neutral-200/75 dark:bg-neutral-800/75' },
                    container: 'items-center',
                }"
                v-model="isOpen"
                prevent-close
            >
                <UCard class="sm:w-72 md:w-96 dark:bg-neutral-900">
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">Add Location</h3>
                        <UButton
                            color="gray"
                            variant="ghost"
                            icon="i-heroicons-x-mark-20-solid"
                            class="-my-1 dark:bg-neutral-800"
                            @click="isOpen = false"
                            size="2xs"
                        />
                    </div>
                    <!-- TODO Fix for the light theme -->
                    <UDropdown
                        v-model:open="open"
                        :items="items"
                        :popper="{ placement: 'bottom-start' }"
                        :ui="{ wrapper: 'w-full' }"
                        width="w-full"
                    >
                        <UInput
                            v-model="name"
                            name="name"
                            placeholder="Search..."
                            icon="i-heroicons-magnifying-glass-20-solid"
                            autocomplete="off"
                            :ui="{ icon: { trailing: { pointer: '' } }, wrapper: 'w-full h-10 ', base: 'h-full' }"
                            variant="none"
                            :class="`dark:bg-neutral-800 dark:rounded-md ${errorMessage && 'border-2 border-red-600'}`"
                            @keyup.enter="addLocation"
                        >
                            <template #trailing>
                                <UButton
                                    v-show="name !== ''"
                                    color="gray"
                                    variant="link"
                                    icon="i-heroicons-x-mark-20-solid"
                                    :padded="false"
                                    @click="name = ''"
                                />
                            </template>
                        </UInput>
                    </UDropdown>

                    <div class="text-xs text-red-600" v-if="errorMessage">
                        {{ errorMessage }}
                    </div>
                    <UButton
                        :loading="loading"
                        color="primary"
                        variant="solid"
                        size="md"
                        label="Add Location"
                        class="w-full flex justify-center mt-3 font-bold dark:bg-blue-100 dark:hover:bg-blue-200"
                        @click="addLocation"
                    />
                </UCard>
            </UModal>
        </div>
    </UContainer>
</template>

<script setup lang="ts">
interface item {
    label: string;
    click: () => void;
}

const isOpen = ref(false);
const name = ref('');
const open = ref(false);
const items = ref<item[][]>([]);
const errorMessage = ref('');
// we are using the useToast hook to show a toast message
const toast = useToast();
const loading = ref(false);

const handleClose = () => {
    isOpen.value = false;
    name.value = '';
};
const addLocation = async () => {
    // we are checking if the name is less than 3 characters
    if (name.value.length <= 2) {
        errorMessage.value = 'Name must be at least 3 characters';
        return;
    }
    loading.value = true;
    await $fetch('http://127.0.0.1:8000/locations', {
        method: 'POST',
        body: JSON.stringify({ name: name.value }),
        onResponse: ({ response }) => {
            // success case
            if (response.status === 201) {
                isOpen.value = false;
                name.value = '';
                loading.value = false;
                refreshNuxtData('locations');
                toast.add({
                    title: 'Location added',
                });
            } else if (response.status === 404) {
                // error case if the location is not found
                errorMessage.value = 'Location not found';
                loading.value = false;
                toast.add({
                    title: 'Location not found',
                });
            } else if (response.status === 300) {
                // error case if there is multiple locations with the same input (I am enabling users to add locations like if they input pari it will add paris because it is the only valid location with the input)
                errorMessage.value = 'Please specify the name of the location';
                loading.value = false;
                toast.add({
                    title: 'Please specify the name of the location',
                });
            } else {
                // error case if the location already exists
                errorMessage.value = 'Location already exists';
                loading.value = false;
                toast.add({
                    title: 'Location already exists',
                });
            }
        },
    });
};

const searchLocation = async () => {
    items.value = [];
    if (name.value.length <= 2) return;
    open.value = true;
    await $fetch(`http://127.0.0.1:8000/search/${name.value}`, {
        method: 'GET',
        onResponse: ({ response }) => {
            for (const item of response._data) {
                items.value.push([
                    {
                        label: item[0],
                        click: () => {
                            name.value = item[0];
                        },
                    },
                ]);
            }
        },
    });
};

watch(name, () => {
    errorMessage.value = '';
    searchLocation();
});
</script>
