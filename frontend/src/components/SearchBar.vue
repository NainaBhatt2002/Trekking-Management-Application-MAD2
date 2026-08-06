<template>
  <div class="input-group shadow-sm rounded">
    <span class="input-group-text bg-white border-end-0">
      <i class="bi bi-search text-secondary"></i>
    </span>

    <input
      type="text"
      class="form-control border-start-0 shadow-none py-2"
      :value="modelValue"
      :placeholder="placeholder"
      @input="emit('update:modelValue', $event.target.value)"
    />

    <button
      v-if="modelValue"
      type="button"
      class="btn btn-white border border-start-0 text-secondary"
      @click="clearSearch"
      title="Clear Search"
    >
      <i class="bi bi-x-circle-fill"></i>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "Search...",
  },
});

const emit = defineEmits(["update:modelValue"]);

const clearSearch = () => {
  emit("update:modelValue", "");
};
</script>