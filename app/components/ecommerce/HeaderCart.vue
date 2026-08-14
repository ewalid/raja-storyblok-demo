<script setup>
/**
 * Header shopping cart (display-only): a cart button + dropdown listing line
 * items, quantities, remove buttons and total. Backed by the Shopify Cart API
 * via useCart, with the cart id persisted in a `shopify-cart-id` cookie.
 * Rendered only when the cart is enabled in site-config.
 *
 * This component also owns cart initialisation (cookie load + persistence), so
 * it stays mounted at every breakpoint even when hidden — the mobile drawer
 * reuses the same shared cart state.
 */
defineProps({ light: Boolean });

const cartIdCookie = useCookie('shopify-cart-id');
const { cart, cartId, cartOpen, toggleCart, closeCart, getCart } = useCart();

// Initialise on the client (SSR is disabled) to avoid a Suspense boundary.
onMounted(async () => {
  try {
    await getCart(cartIdCookie.value);
  }
  catch (error) {
    console.log(error);
  }
});

watchEffect(() => {
  if (cartId.value) {
    cartIdCookie.value = cartId.value;
  }
});
</script>

<template>
  <div class="relative flex h-full items-center">
    <button
      class="focus-ring flex items-center space-x-2"
      :class="light ? 'text-primary-dark' : 'text-white'"
      aria-label="Open cart"
      @click.prevent="toggleCart"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="pointer-events-none block size-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z"
        />
      </svg>
      <span class="text-sm">Cart ({{ cart?.quantity || '0' }})</span>
    </button>
    <Transition name="fade">
      <div
        v-show="cartOpen"
        class="absolute right-0 top-full w-[320px] rounded-lg bg-white px-6 pb-6 pt-10 shadow-lg"
      >
        <button
          class="focus-ring absolute right-2 top-2 text-primary-dark"
          aria-label="Close cart"
          @click="closeCart()"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-6"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div
          class="pointer-events-none absolute right-6 top-0 size-4 -translate-y-1/2 rotate-45 bg-white"
        ></div>
        <EcommerceCartPanel />
      </div>
    </Transition>
  </div>
</template>

<style scoped>
@reference "~/assets/css/tailwind.css";

.fade-enter-active,
.fade-leave-active {
  @apply transition-all duration-300;
}

.fade-enter-from,
.fade-leave-to {
  @apply -translate-y-2 opacity-0;
}
</style>
