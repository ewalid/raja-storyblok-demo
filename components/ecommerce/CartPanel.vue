<script setup>
/**
 * Presentational cart contents (line items, remove buttons, total) shared by
 * the header dropdown (desktop) and the mobile nav drawer. Reads the shared
 * cart state from useCart.
 */
const { cart, removeFromCart } = useCart();
</script>

<template>
  <div v-if="cart?.items?.length" class="flex flex-col space-y-2 text-primary-dark">
    <div class="flex flex-row text-sm">
      <span class="w-[40px] font-black">Qty</span>
      <span class="grow font-black">Product</span>
      <span class="w-[80px] text-right font-black">Price</span>
      <span class="w-[28px]"></span>
    </div>
    <div v-for="item in cart.items" :key="item.id" class="flex flex-row items-center text-sm">
      <span class="w-[40px]">{{ item.quantity }}</span>
      <span class="grow">{{ item.title }}</span>
      <span class="w-[80px] text-right">{{ item.price }} {{ cart.currency }}</span>
      <button
        class="focus-ring text-primary-dark/60 ml-1 flex w-[28px] justify-end transition-colors hover:text-primary-dark"
        :aria-label="`Remove ${item.title}`"
        @click="removeFromCart(item.id)"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-4"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <div class="flex flex-row border-t border-primary-dark pt-2 font-black">
      <span class="grow">Total</span>
      <span v-if="cart.total > 0" class="text-right">{{ cart.total }} {{ cart.currency }}</span>
    </div>
    <!-- Decorative only — no checkout flow in this demo. -->
    <button
      type="button"
      class="focus-ring mt-2 w-full cursor-pointer rounded-md border-2 border-primary-dark bg-primary-dark px-6 py-2 text-center font-semibold tracking-wider text-white transition-all duration-300 hover:scale-[1.02]"
    >
      Checkout
    </button>
  </div>
  <p v-else class="text-sm text-primary-dark">Your cart is empty.</p>
</template>
