from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape
import json

class ListStringWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - ListStringWidget */
        #cms-list-{id_str} {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        }}
        .cms-widget-container {{
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }}
        .cms-card {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #1e293b !important;
        }}
        .cms-card-title {{
            color: #0f172a !important;
        }}
        .cms-input-field {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }}
        .cms-input-field::placeholder {{
            color: #94a3b8 !important;
        }}
        .cms-form-box {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }}
        
        /* Dark Mode overrides with elevated specificity */
        html.dark .cms-widget-container,
        body.dark .cms-widget-container,
        .dark .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark .cms-card,
        body.dark .cms-card,
        .dark .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark .cms-card-title,
        body.dark .cms-card-title,
        .dark .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field,
        body.dark .cms-input-field,
        .dark .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field::placeholder,
        body.dark .cms-input-field::placeholder,
        .dark .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark .cms-form-box,
        body.dark .cms-form-box,
        .dark .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        </style>

        <div id="cms-list-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newItem: '',
                 addItem() {{
                     if (this.newItem.trim()) {{
                         this.items.push(this.newItem.trim());
                         this.newItem = '';
                     }}
                 }},
                 removeItem(idx) {{
                     this.items.splice(idx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-3 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- List of items -->
            <div class="space-y-2 max-h-64 overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card flex items-center justify-between gap-3 p-3 border rounded-xl shadow-sm hover:border-slate-350 transition-colors">
                        <span class="cms-card-title text-xs font-medium" x-text="item"></span>
                        <button type="button" class="text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeItem(idx)">
                            <span class="material-symbols-outlined align-middle" style="font-size: 18px;">delete</span>
                        </button>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No items added yet.</p>
                </div>
            </div>
            
            <!-- Add Item Input Form -->
            <div class="cms-form-box flex gap-2 mt-4 p-2 border rounded-xl shadow-sm">
                <input type="text" x-model="newItem" @keydown.enter.prevent="addItem()" placeholder="Add new item..." 
                       class="cms-input-field flex-1 text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                <button type="button" @click="addItem()" 
                        class="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add
                </button>
            </div>
        </div>
        """
        return mark_safe(html)

class ConditionsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                items = json.loads(value)
            except Exception:
                items = []
        elif isinstance(value, list):
            items = value
        else:
            items = []
            
        items_json = json.dumps(items)
        items_json_escaped = escape(items_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - ConditionsWidget */
        #cms-cond-{id_str} {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        }}
        .cms-widget-container {{
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }}
        .cms-card {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #1e293b !important;
        }}
        .cms-card-title {{
            color: #0f172a !important;
        }}
        .cms-card-desc, .cms-card-desc * {{
            color: #475569 !important;
        }}
        .cms-input-field {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #0f172a !important;
        }}
        .cms-input-field::placeholder {{
            color: #94a3b8 !important;
        }}
        .cms-form-box {{
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }}
        
        /* Dark Mode overrides with elevated specificity */
        html.dark .cms-widget-container,
        body.dark .cms-widget-container,
        .dark .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark .cms-card,
        body.dark .cms-card,
        .dark .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark .cms-card-title,
        body.dark .cms-card-title,
        .dark .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark .cms-card-desc,
        html.dark .cms-card-desc *,
        body.dark .cms-card-desc,
        body.dark .cms-card-desc *,
        .dark .cms-card-desc,
        .dark .cms-card-desc * {{
            color: #94a3b8 !important;
        }}
        html.dark .cms-input-field,
        body.dark .cms-input-field,
        .dark .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark .cms-input-field::placeholder,
        body.dark .cms-input-field::placeholder,
        .dark .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark .cms-form-box,
        body.dark .cms-form-box,
        .dark .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        /* Specific overrides for Unfold's dark mode styling in labels */
        html.dark .cms-label,
        body.dark .cms-label,
        .dark .cms-label {{
            color: #94a3b8 !important;
        }}
        </style>

        <div id="cms-cond-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newTitle: '',
                 newIcon: '',
                 newDesc: '',
                 addItem() {{
                     let desc = this.newDesc.trim();
                     if (this.newTitle.trim() && desc) {{
                         this.items.push({{
                             id: this.items.length + 1,
                             title: this.newTitle.trim(),
                             description: desc,
                             icon: this.newIcon.trim() || `<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' width='22' height='22'><path d='M5 12h14M12 5l7 7-7 7' /></svg>`
                         }});
                         this.newTitle = '';
                         this.newIcon = '';
                         this.newDesc = '';
                     }}
                 }},
                 removeItem(idx) {{
                     this.items.splice(idx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-3 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <!-- List of items -->
            <div class="space-y-3 max-h-80 overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-3 border rounded-xl shadow-sm relative space-y-1 hover:border-slate-350 transition-colors">
                        <button type="button" class="absolute top-2 right-2 text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeItem(idx)">
                            <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                        </button>
                        <p class="cms-card-title text-xs font-semibold pr-6 leading-normal" x-text="item.title"></p>
                        <div class="cms-card-desc text-[10px] leading-relaxed pt-1.5 border-t border-slate-50 mt-1" x-html="item.description"></div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No conditions added yet.</p>
                </div>
            </div>
            
            <!-- Add Item Input Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add Condition Card</h4>
                <div class="grid sm:grid-cols-2 gap-3">
                    <input type="text" x-model="newTitle" placeholder="Condition Title (e.g. Back pain)" 
                           class="cms-input-field text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                    <input type="text" x-model="newIcon" placeholder="SVG Icon Code (Optional)" 
                           class="cms-input-field text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 font-mono transition-colors" />
                </div>
                
                <div class="space-y-1">
                    <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Card Description</label>
                    <textarea id="cond-desc-{id_str}" x-model="newDesc" rows="2" placeholder="Condition Description..." 
                              class="cms-input-field w-full text-xs px-3 py-2.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors"></textarea>
                </div>

                <button type="button" @click="addItem()" 
                        class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add Condition Card
                </button>
            </div>
        </div>
        """
        return mark_safe(html)
