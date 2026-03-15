<template>
  <div class="tag-input-container">
    <el-input
      v-model="inputValue"
      type="textarea"
      :rows="3"
      placeholder="请输入标签，多个标签用逗号分隔"
      @input="handleInput"
    ></el-input>
    <div class="tag-list" v-if="tags.length > 0">
      <el-tag
        v-for="tag in tags"
        :key="tag"
        size="small"
        close-transition
      >
        {{ tag }}
      </el-tag>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const inputValue = ref(props.modelValue)
const tags = ref([])

const handleInput = () => {
  // 分割标签并去重
  const tagArray = inputValue.value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag)
  const uniqueTags = [...new Set(tagArray)]
  tags.value = uniqueTags
  emit('update:modelValue', uniqueTags.join(','))
}

// 监听外部 modelValue 变化
watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue
    handleInput()
  },
  { immediate: true }
)
</script>

<style scoped>
.tag-input-container {
  margin-bottom: 16px;
}

.tag-list {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
