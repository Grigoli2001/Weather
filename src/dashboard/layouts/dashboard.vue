<template>
    <div>
        <UContainer class="mt-4">
            <header class="flex items-center">
                <div class="relative h-fit w-fit px-2 mr-2">
                    <div class="flex h-full">
                        <img src="~assets/icons/1.svg" alt="" class="h-full" />
                    </div>
                    <img src="~assets/icons/4.svg" alt="" class="absolute w-fit size-[60%] right-0 top-0 opacity-70" />
                    <img
                        src="~assets/icons/4.svg"
                        alt=""
                        class="absolute w-fit size-[70%] bottom-0 left-0 opacity-90"
                    />
                </div>
                <h1 class="text-base font-medium">Weather App</h1>
            </header>
        </UContainer>

        <main>
            <slot />
        </main>
    </div>
</template>
