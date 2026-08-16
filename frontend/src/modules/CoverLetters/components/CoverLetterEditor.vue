<template>
  <div class="cover-letter-editor">
    <div v-if="editor" class="editor-toolbar">
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isBold }]"
        @click="editor!.chain().focus().toggleBold().run()"
      >
        <q-icon name="format_bold" size="18px" />
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isItalic }]"
        @click="editor!.chain().focus().toggleItalic().run()"
      >
        <q-icon name="format_italic" size="18px" />
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isUnderline }]"
        @click="editor!.chain().focus().toggleUnderline().run()"
      >
        <q-icon name="format_underlined" size="18px" />
      </q-btn>
      <q-separator vertical class="q-mx-xs" />
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isH1 }]"
        @click="editor!.chain().focus().toggleHeading({ level: 1 }).run()"
      >
        H1
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isH2 }]"
        @click="editor!.chain().focus().toggleHeading({ level: 2 }).run()"
      >
        H2
      </q-btn>
      <q-separator vertical class="q-mx-xs" />
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isBulletList }]"
        @click="editor!.chain().focus().toggleBulletList().run()"
      >
        <q-icon name="format_list_bulleted" size="18px" />
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isOrderedList }]"
        @click="editor!.chain().focus().toggleOrderedList().run()"
      >
        <q-icon name="format_list_numbered" size="18px" />
      </q-btn>
      <q-separator vertical class="q-mx-xs" />
      <q-btn
        flat
        dense
        no-caps
        unelevated
        :class="['toolbar-btn', { 'toolbar-btn--active': isBlockquote }]"
        @click="editor!.chain().focus().toggleBlockquote().run()"
      >
        <q-icon name="format_quote" size="18px" />
      </q-btn>
      <q-btn flat dense no-caps unelevated class="toolbar-btn" @click="setLink">
        <q-icon name="link" size="18px" />
      </q-btn>
      <q-separator vertical class="q-mx-xs" />
      <q-btn
        flat
        dense
        no-caps
        unelevated
        class="toolbar-btn"
        @click="editor!.chain().focus().setHorizontalRule().run()"
      >
        <q-icon name="horizontal_rule" size="18px" />
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        class="toolbar-btn"
        :disable="!editor!.can().undo()"
        @click="editor!.chain().focus().undo().run()"
      >
        <q-icon name="undo" size="18px" />
      </q-btn>
      <q-btn
        flat
        dense
        no-caps
        unelevated
        class="toolbar-btn"
        :disable="!editor!.can().redo()"
        @click="editor!.chain().focus().redo().run()"
      >
        <q-icon name="redo" size="18px" />
      </q-btn>
    </div>
    <EditorContent :editor="editor as any" class="editor-content" />
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, watch } from "vue";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import Underline from "@tiptap/extension-underline";
import Link from "@tiptap/extension-link";
import TextAlign from "@tiptap/extension-text-align";

const props = defineProps<{
  modelValue: string | null;
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: string | null): void;
}>();

const editor = useEditor({
  content: props.modelValue ?? "",
  extensions: [
    StarterKit.configure({
      heading: { levels: [1, 2] }
    }),
    Placeholder.configure({
      placeholder: "Write your cover letter content..."
    }),
    Underline,
    Link.configure({
      openOnClick: false,
      HTMLAttributes: { class: "editor-link" }
    }),
    TextAlign.configure({
      types: ["heading", "paragraph"]
    })
  ],
  onUpdate: ({ editor: e }) => {
    const html = e.getHTML();
    emit("update:modelValue", html === "<p></p>" ? null : html);
  }
});

const isBold = computed(() => editor.value?.isActive("bold") ?? false);
const isItalic = computed(() => editor.value?.isActive("italic") ?? false);
const isUnderline = computed(
  () => editor.value?.isActive("underline") ?? false
);
const isH1 = computed(
  () => editor.value?.isActive("heading", { level: 1 }) ?? false
);
const isH2 = computed(
  () => editor.value?.isActive("heading", { level: 2 }) ?? false
);
const isBulletList = computed(
  () => editor.value?.isActive("bulletList") ?? false
);
const isOrderedList = computed(
  () => editor.value?.isActive("orderedList") ?? false
);
const isBlockquote = computed(
  () => editor.value?.isActive("blockquote") ?? false
);

function setLink() {
  if (!editor.value) return;
  const previousUrl = editor.value.getAttributes("link").href;
  const url = window.prompt("Enter URL", previousUrl);
  if (url === null) return;
  if (url === "") {
    editor.value.chain().focus().extendMarkRange("link").unsetLink().run();
    return;
  }
  editor.value
    .chain()
    .focus()
    .extendMarkRange("link")
    .setLink({ href: url })
    .run();
}

watch(
  () => props.modelValue,
  value => {
    if (!editor.value) return;
    const current = editor.value.getHTML();
    if (current !== value) {
      editor.value.commands.setContent(value ?? "");
    }
  }
);

onBeforeUnmount(() => {
  editor.value?.destroy();
});
</script>

<style lang="scss" scoped>
.cover-letter-editor {
  border: 1px solid #dce6eb;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  transition: border-color 0.2s;
}
.cover-letter-editor:focus-within {
  border-color: var(--cv-primary);
}
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 10px;
  border-bottom: 1px solid #edf2f5;
  background: #f8fafc;
  flex-wrap: wrap;
}
.toolbar-btn {
  min-width: 32px;
  min-height: 32px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  color: var(--cv-muted);
}
.toolbar-btn--active {
  background: var(--cv-primary-soft) !important;
  color: var(--cv-primary-dark) !important;
}
.editor-content {
  min-height: 200px;
  max-height: 500px;
  overflow-y: auto;
  padding: 14px 16px;
}
.editor-content :deep(.tiptap) {
  outline: none;
  min-height: 170px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--cv-text-strong);
}
.editor-content :deep(.tiptap p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  color: var(--cv-muted-light);
  pointer-events: none;
  height: 0;
}
.editor-content :deep(.tiptap h1) {
  font-size: 20px;
  font-weight: 800;
  margin: 16px 0 8px;
  color: var(--cv-navy);
}
.editor-content :deep(.tiptap h2) {
  font-size: 16px;
  font-weight: 800;
  margin: 14px 0 6px;
  color: var(--cv-navy);
}
.editor-content :deep(.tiptap ul),
.editor-content :deep(.tiptap ol) {
  padding-left: 24px;
  margin: 8px 0;
}
.editor-content :deep(.tiptap li) {
  margin: 2px 0;
}
.editor-content :deep(.tiptap blockquote) {
  border-left: 3px solid var(--cv-primary);
  margin: 12px 0;
  padding: 8px 16px;
  background: #f8fafc;
  border-radius: 0 8px 8px 0;
  color: var(--cv-muted);
  font-style: italic;
}
.editor-content :deep(.tiptap hr) {
  border: none;
  border-top: 1px solid #dce6eb;
  margin: 16px 0;
}
.editor-content :deep(.tiptap a) {
  color: var(--cv-primary-dark);
  text-decoration: underline;
  cursor: pointer;
}
.editor-content :deep(.tiptap a:hover) {
  color: var(--cv-primary);
}
</style>
