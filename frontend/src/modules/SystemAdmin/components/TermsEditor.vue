<template>
  <div class="terms-editor">
    <div v-if="editor" class="editor-toolbar" aria-label="Text formatting">
      <q-btn
        v-for="action in markActions"
        :key="action.label"
        flat
        dense
        :icon="action.icon"
        :aria-label="action.label"
        :class="['toolbar-btn', { active: action.active() }]"
        @click="action.run()"
      />
      <q-separator vertical inset />
      <q-btn
        flat
        dense
        label="H1"
        :class="[
          'toolbar-btn',
          { active: editor.isActive('heading', { level: 1 }) }
        ]"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
      />
      <q-btn
        flat
        dense
        label="H2"
        :class="[
          'toolbar-btn',
          { active: editor.isActive('heading', { level: 2 }) }
        ]"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
      />
      <q-separator vertical inset />
      <q-btn
        flat
        dense
        icon="format_list_bulleted"
        aria-label="Bullet list"
        :class="['toolbar-btn', { active: editor.isActive('bulletList') }]"
        @click="editor.chain().focus().toggleBulletList().run()"
      />
      <q-btn
        flat
        dense
        icon="format_list_numbered"
        aria-label="Numbered list"
        :class="['toolbar-btn', { active: editor.isActive('orderedList') }]"
        @click="editor.chain().focus().toggleOrderedList().run()"
      />
      <q-btn
        flat
        dense
        icon="format_quote"
        aria-label="Quote"
        :class="['toolbar-btn', { active: editor.isActive('blockquote') }]"
        @click="editor.chain().focus().toggleBlockquote().run()"
      />
      <q-btn
        flat
        dense
        icon="link"
        aria-label="Add link"
        class="toolbar-btn"
        @click="setLink"
      />
      <q-separator vertical inset />
      <q-btn
        flat
        dense
        icon="undo"
        aria-label="Undo"
        class="toolbar-btn"
        :disable="!editor.can().undo()"
        @click="editor.chain().focus().undo().run()"
      />
      <q-btn
        flat
        dense
        icon="redo"
        aria-label="Redo"
        class="toolbar-btn"
        :disable="!editor.can().redo()"
        @click="editor.chain().focus().redo().run()"
      />
    </div>
    <EditorContent :editor="editor as any" class="editor-content" />
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, watch } from "vue";
import { EditorContent, useEditor } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import Underline from "@tiptap/extension-underline";
import Link from "@tiptap/extension-link";

const props = defineProps<{ modelValue: string }>();
const emit = defineEmits<{
  (event: "update:modelValue", value: string): void;
}>();

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
    Placeholder.configure({
      placeholder: "Write the Terms of Service shown to new users…"
    }),
    Underline,
    Link.configure({ openOnClick: false })
  ],
  onUpdate: ({ editor: instance }) => {
    emit("update:modelValue", instance.getHTML());
  }
});

const markActions = computed(() => [
  {
    label: "Bold",
    icon: "format_bold",
    active: () => editor.value?.isActive("bold") ?? false,
    run: () => editor.value?.chain().focus().toggleBold().run()
  },
  {
    label: "Italic",
    icon: "format_italic",
    active: () => editor.value?.isActive("italic") ?? false,
    run: () => editor.value?.chain().focus().toggleItalic().run()
  },
  {
    label: "Underline",
    icon: "format_underlined",
    active: () => editor.value?.isActive("underline") ?? false,
    run: () => editor.value?.chain().focus().toggleUnderline().run()
  }
]);

function setLink() {
  if (!editor.value) return;
  const current = editor.value.getAttributes("link").href as string | undefined;
  const url = window.prompt("Enter a link URL", current ?? "https://");
  if (url === null) return;
  if (!url.trim()) {
    editor.value.chain().focus().extendMarkRange("link").unsetLink().run();
    return;
  }
  editor.value
    .chain()
    .focus()
    .extendMarkRange("link")
    .setLink({ href: url.trim() })
    .run();
}

watch(
  () => props.modelValue,
  value => {
    if (editor.value && editor.value.getHTML() !== value) {
      editor.value.commands.setContent(value);
    }
  }
);

onBeforeUnmount(() => editor.value?.destroy());
</script>

<style scoped lang="scss">
.terms-editor {
  overflow: hidden;
  border: 1px solid #dbe2e9;
  border-radius: 11px;
  background: #fff;
}
.terms-editor:focus-within {
  border-color: #1769e0;
  box-shadow: 0 0 0 2px rgba(23, 105, 224, 0.08);
}
.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 3px;
  padding: 7px 10px;
  border-bottom: 1px solid #e5eaf0;
  background: #f7f9fc;
}
.toolbar-btn {
  min-width: 33px;
  min-height: 33px;
  border-radius: 6px;
  color: #68768a;
  font-size: 11px;
  font-weight: 800;
}
.toolbar-btn.active {
  color: #1769e0;
  background: #e8f1ff;
}
.editor-content {
  min-height: 390px;
  max-height: 600px;
  overflow-y: auto;
  padding: 22px 25px;
}
.editor-content :deep(.tiptap) {
  min-height: 345px;
  outline: none;
  color: #445166;
  font-size: 14px;
  line-height: 1.7;
}
.editor-content :deep(.tiptap p.is-editor-empty:first-child::before) {
  float: left;
  height: 0;
  color: #9aa4b2;
  content: attr(data-placeholder);
  pointer-events: none;
}
.editor-content :deep(h1) {
  color: #172033;
  font-size: 24px;
}
.editor-content :deep(h2) {
  margin-top: 22px;
  color: #263449;
  font-size: 18px;
}
.editor-content :deep(h3) {
  color: #344258;
  font-size: 15px;
}
.editor-content :deep(a) {
  color: #1769e0;
}
</style>
