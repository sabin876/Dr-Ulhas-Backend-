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

class CommonlyTreatedWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
        # Load existing JSON value or default to empty list
        if isinstance(value, str):
            try:
                categories = json.loads(value)
            except Exception:
                categories = []
        elif isinstance(value, list):
            categories = value
        else:
            categories = []
            
        categories_json = json.dumps(categories)
        categories_json_escaped = escape(categories_json)
        
        html = f"""
        <style>
        /* CMS Widget Theme System - CommonlyTreatedWidget */
        #cms-treated-{id_str} {{
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
        
        /* Dark Mode overrides */
        html.dark #cms-treated-{id_str} .cms-widget-container,
        body.dark #cms-treated-{id_str} .cms-widget-container,
        .dark #cms-treated-{id_str} .cms-widget-container {{
            background-color: #0f172a !important;
            border-color: #1e293b !important;
        }}
        html.dark #cms-treated-{id_str} .cms-card,
        body.dark #cms-treated-{id_str} .cms-card,
        .dark #cms-treated-{id_str} .cms-card {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
            color: #cbd5e1 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-card-title,
        body.dark #cms-treated-{id_str} .cms-card-title,
        .dark #cms-treated-{id_str} .cms-card-title {{
            color: #f8fafc !important;
        }}
        html.dark #cms-treated-{id_str} .cms-input-field,
        body.dark #cms-treated-{id_str} .cms-input-field,
        .dark #cms-treated-{id_str} .cms-input-field {{
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }}
        html.dark #cms-treated-{id_str} .cms-input-field::placeholder,
        body.dark #cms-treated-{id_str} .cms-input-field::placeholder,
        .dark #cms-treated-{id_str} .cms-input-field::placeholder {{
            color: #475569 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-form-box,
        body.dark #cms-treated-{id_str} .cms-form-box,
        .dark #cms-treated-{id_str} .cms-form-box {{
            background-color: #1e293b !important;
            border-color: #334155 !important;
        }}
        html.dark #cms-treated-{id_str} .cms-label,
        body.dark #cms-treated-{id_str} .cms-label,
        .dark #cms-treated-{id_str} .cms-label {{
            color: #94a3b8 !important;
        }}
        </style>
        
        <div id="cms-treated-{id_str}" 
             x-data="{{ 
                 categories: {categories_json_escaped},
                 newCatTitle: '',
                 newCatIcon: 'PlusSquare',
                 newCatItemsText: '',
                 
                 addCategory() {{
                     let title = this.newCatTitle.trim();
                     if (!title) {{
                         alert('Category title cannot be empty.');
                         return;
                     }}
                     if (this.categories.some(cat => cat.title.toLowerCase() === title.toLowerCase())) {{
                         alert('A category with this title already exists.');
                         return;
                     }}
                     let itemsList = [];
                     if (this.newCatItemsText.trim()) {{
                         itemsList = this.newCatItemsText.split(/[\\n,]+/).map(item => item.trim()).filter(item => item.length > 0);
                     }}
                     this.categories.push({{
                         title: title,
                         icon: this.newCatIcon,
                         items: itemsList
                     }});
                     this.newCatTitle = '';
                     this.newCatIcon = 'PlusSquare';
                     this.newCatItemsText = '';
                 }},
                 removeCategory(idx) {{
                     if (confirm('Are you sure you want to remove this category?')) {{
                         this.categories.splice(idx, 1);
                     }}
                 }},
                 
                 // Add item dynamically to existing category
                 newItemText: {{}},
                 addItem(catIdx) {{
                     let text = (this.newItemText[catIdx] || '').trim();
                     if (!text) return;
                     if (this.categories[catIdx].items.some(item => item.toLowerCase() === text.toLowerCase())) {{
                         alert('This item already exists in this category.');
                         return;
                     }}
                     this.categories[catIdx].items.push(text);
                     this.newItemText[catIdx] = '';
                 }},
                 removeItem(catIdx, itemIdx) {{
                     this.categories[catIdx].items.splice(itemIdx, 1);
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <!-- Hidden original textarea that Django reads/writes -->
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(categories)">{categories_json_escaped}</textarea>
            
            <!-- List of Categories -->
            <div class="space-y-4 max-h-[400px] overflow-y-auto pr-1">
                <template x-for="(cat, catIdx) in categories" :key="catIdx">
                    <div class="cms-card p-4 border rounded-xl shadow-sm relative space-y-3 hover:border-slate-350 transition-colors">
                        <!-- Header with Title & Icon & Delete Button -->
                        <div class="flex items-center justify-between border-b border-slate-100 pb-2 gap-3">
                            <div class="flex flex-wrap items-center gap-3 flex-1">
                                <div class="flex items-center gap-1.5">
                                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Title:</span>
                                    <input type="text" x-model="cat.title" placeholder="Category Title"
                                           class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg w-full max-w-[150px] focus:outline-none focus:border-sky-500 transition-colors" />
                                </div>
                                <div class="flex items-center gap-1.5">
                                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Icon:</span>
                                    <select x-model="cat.icon" 
                                            class="cms-input-field text-[11px] px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors">
                                        <option value="PlusSquare">PlusSquare (Upper)</option>
                                        <option value="Triangle">Triangle (Lower)</option>
                                        <option value="Hexagon">Hexagon (Joint/Complex)</option>
                                        <option value="ShieldCheck">ShieldCheck</option>
                                        <option value="Activity">Activity</option>
                                        <option value="Zap">Zap</option>
                                        <option value="HeartPulse">HeartPulse</option>
                                    </select>
                                </div>
                            </div>
                            <button type="button" class="text-red-500 hover:bg-red-50 p-1 rounded-lg border-0 bg-transparent flex items-center justify-center cursor-pointer transition-colors" @click="removeCategory(catIdx)">
                                <span class="material-symbols-outlined align-middle" style="font-size: 18px;">delete</span>
                            </button>
                        </div>
                        
                        <!-- List of items under this category -->
                        <div class="space-y-1.5 pl-2">
                            <template x-for="(item, itemIdx) in cat.items" :key="itemIdx">
                                <div class="flex items-center justify-between text-xs text-slate-600 dark:text-slate-300 py-1 px-2 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg gap-2">
                                    <div class="flex items-center gap-2 flex-1">
                                        <span class="w-1.5 h-1.5 bg-sky-500 rounded-full flex-shrink-0"></span>
                                        <input type="text" x-model="cat.items[itemIdx]"
                                               class="cms-input-field text-xs bg-transparent border-0 border-b border-slate-100 hover:border-slate-200 focus:border-sky-500 focus:outline-none w-full py-0.5" />
                                    </div>
                                    <button type="button" class="text-red-400 hover:text-red-650 border-0 bg-transparent cursor-pointer p-0.5 flex items-center justify-center flex-shrink-0" @click="removeItem(catIdx, itemIdx)">
                                        <span class="material-symbols-outlined align-middle" style="font-size: 14px;">close</span>
                                    </button>
                                </div>
                            </template>
                            <div x-show="!cat.items || cat.items.length === 0">
                                <p class="text-[10px] text-slate-400 italic">No items in this category.</p>
                            </div>
                        </div>
                        
                        <!-- Add Inline Item Form -->
                        <div class="flex gap-2 pt-2 border-t border-slate-50 mt-2">
                            <input type="text" 
                                   x-model="newItemText[catIdx]" 
                                   @keydown.enter.prevent="addItem(catIdx)" 
                                   placeholder="Add new item to this category..." 
                                   class="cms-input-field flex-1 text-[11px] px-2 py-1.5 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                            <button type="button" 
                                    @click="addItem(catIdx)"
                                    class="px-3 py-1 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[9px] rounded-lg transition-all uppercase tracking-wider border-0 cursor-pointer">
                                Add Item
                            </button>
                        </div>
                    </div>
                </template>
                <div x-show="categories.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No categories added yet.</p>
                </div>
            </div>
            
            <!-- Add New Category Form -->
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add New Category</h4>
                <div class="grid sm:grid-cols-2 gap-3">
                    <div class="space-y-1">
                        <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Category Title</label>
                        <input type="text" x-model="newCatTitle" placeholder="Category Title (e.g. Upper Limb)" 
                               class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors" />
                    </div>
                    <div class="space-y-1">
                        <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Icon Type</label>
                        <select x-model="newCatIcon" 
                                class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors">
                            <option value="PlusSquare">PlusSquare (Upper Limb)</option>
                            <option value="Triangle">Triangle (Lower Limb)</option>
                            <option value="Hexagon">Hexagon (Joint & Complex Trauma)</option>
                            <option value="ShieldCheck">ShieldCheck</option>
                            <option value="Activity">Activity</option>
                            <option value="Zap">Zap</option>
                            <option value="HeartPulse">HeartPulse</option>
                        </select>
                    </div>
                </div>
                
                <div class="space-y-1">
                    <label class="cms-label text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Initial Items (comma or newline separated)</label>
                    <textarea x-model="newCatItemsText" rows="2" placeholder="Item 1&#10;Item 2&#10;Item 3" 
                              class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg focus:outline-none focus:border-sky-500 transition-colors"></textarea>
                </div>

                <button type="button" @click="addCategory()" 
                        class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg shadow-sm transition-all uppercase tracking-wider border-0 cursor-pointer">
                    Add Category
                </button>
            </div>
        </div>
        """
        return mark_safe(html)



class JourneyStepsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        id_str = attrs.get('id', name)
        
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
        
        html = f'''
        <style>
        #cms-journey-{id_str} {{ font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }}
        .cms-widget-container {{ background-color: #f8fafc !important; border-color: #e2e8f0 !important; }}
        .cms-card {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #1e293b !important; }}
        .cms-card-title {{ color: #0f172a !important; }}
        .cms-card-desc {{ color: #475569 !important; }}
        .cms-input-field {{ background-color: #ffffff !important; border-color: #cbd5e1 !important; color: #0f172a !important; }}
        .cms-input-field::placeholder {{ color: #94a3b8 !important; }}
        .cms-form-box {{ background-color: #ffffff !important; border-color: #e2e8f0 !important; }}
        html.dark #cms-journey-{id_str} .cms-widget-container, body.dark #cms-journey-{id_str} .cms-widget-container, .dark #cms-journey-{id_str} .cms-widget-container {{ background-color: #0f172a !important; border-color: #1e293b !important; }}
        html.dark #cms-journey-{id_str} .cms-card, body.dark #cms-journey-{id_str} .cms-card, .dark #cms-journey-{id_str} .cms-card {{ background-color: #1e293b !important; border-color: #334155 !important; color: #cbd5e1 !important; }}
        html.dark #cms-journey-{id_str} .cms-card-title, body.dark #cms-journey-{id_str} .cms-card-title, .dark #cms-journey-{id_str} .cms-card-title {{ color: #f8fafc !important; }}
        html.dark #cms-journey-{id_str} .cms-card-desc, body.dark #cms-journey-{id_str} .cms-card-desc, .dark #cms-journey-{id_str} .cms-card-desc {{ color: #94a3b8 !important; }}
        html.dark #cms-journey-{id_str} .cms-input-field, body.dark #cms-journey-{id_str} .cms-input-field, .dark #cms-journey-{id_str} .cms-input-field {{ background-color: #0f172a !important; border-color: #334155 !important; color: #f8fafc !important; }}
        html.dark #cms-journey-{id_str} .cms-input-field::placeholder, body.dark #cms-journey-{id_str} .cms-input-field::placeholder, .dark #cms-journey-{id_str} .cms-input-field::placeholder {{ color: #475569 !important; }}
        html.dark #cms-journey-{id_str} .cms-form-box, body.dark #cms-journey-{id_str} .cms-form-box, .dark #cms-journey-{id_str} .cms-form-box {{ background-color: #1e293b !important; border-color: #334155 !important; }}
        html.dark #cms-journey-{id_str} .cms-label, body.dark #cms-journey-{id_str} .cms-label, .dark #cms-journey-{id_str} .cms-label {{ color: #94a3b8 !important; }}
        </style>
        
        <div id="cms-journey-{id_str}" 
             x-data="{{ 
                 items: {items_json_escaped},
                 newNum: '',
                 newTitle: '',
                 newDesc: '',
                 newIcon: 'ClipboardList',
                 newColor: 'text-blue-500',
                 newGrad: 'from-blue-500/10 to-blue-500/0',
                 newShadow: 'hover:shadow-blue-500/20',
                 newBorder: 'group-hover:border-blue-200',
                 addItem() {{
                     if (this.newTitle.trim() && this.newDesc.trim()) {{
                         this.items.push({{
                             number: this.newNum.trim() || String(this.items.length + 1).padStart(2, '0'),
                             title: this.newTitle.trim(),
                             description: this.newDesc.trim(),
                             icon: this.newIcon.trim() || 'ClipboardList',
                             color: this.newColor.trim(),
                             gradient: this.newGrad.trim(),
                             shadowHover: this.newShadow.trim(),
                             borderHover: this.newBorder.trim()
                         }});
                         this.newNum = '';
                         this.newTitle = '';
                         this.newDesc = '';
                         this.newIcon = 'ClipboardList';
                     }} else {{
                         alert('Title and Description are required.');
                     }}
                 }},
                 removeItem(idx) {{
                     if (confirm('Remove this step?')) {{
                         this.items.splice(idx, 1);
                     }}
                 }}
             }}"
             class="cms-widget-container space-y-4 font-sans p-5 border rounded-2xl max-w-2xl mt-1"
        >
            <textarea name="{name}" id="{id_str}" style="display:none;" :value="JSON.stringify(items)">{items_json_escaped}</textarea>
            
            <div class="space-y-3 max-h-[400px] overflow-y-auto pr-1">
                <template x-for="(item, idx) in items" :key="idx">
                    <div class="cms-card p-4 border rounded-xl shadow-sm relative space-y-2 hover:border-slate-350 transition-colors">
                        <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                            <div class="flex gap-2 items-center w-full">
                                <span class="text-[10px] text-slate-400">Num:</span>
                                <input type="text" x-model="item.number" class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 w-16" />
                                <span class="text-[10px] text-slate-400 ml-2">Title:</span>
                                <input type="text" x-model="item.title" class="cms-input-field text-xs font-bold px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500 flex-1" />
                            </div>
                            <button type="button" class="text-red-500 hover:bg-red-50 p-1.5 rounded-lg border-0 bg-transparent cursor-pointer ml-2" @click="removeItem(idx)">
                                <span class="material-symbols-outlined align-middle" style="font-size: 16px;">delete</span>
                            </button>
                        </div>
                        <div class="flex flex-col gap-1">
                            <span class="text-[10px] text-slate-400">Description:</span>
                            <textarea x-model="item.description" class="cms-input-field w-full text-xs px-2 py-1 border rounded-lg focus:outline-none focus:border-sky-500" rows="2"></textarea>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <div class="flex items-center gap-1.5"><span class="text-[10px] text-slate-400 w-12">Icon:</span><input type="text" x-model="item.icon" class="cms-input-field text-xs px-2 py-1 border rounded w-full" /></div>
                            <div class="flex items-center gap-1.5"><span class="text-[10px] text-slate-400 w-12">Color:</span><input type="text" x-model="item.color" class="cms-input-field text-xs px-2 py-1 border rounded w-full" /></div>
                            <div class="flex items-center gap-1.5"><span class="text-[10px] text-slate-400 w-12">Grad:</span><input type="text" x-model="item.gradient" class="cms-input-field text-xs px-2 py-1 border rounded w-full" /></div>
                            <div class="flex items-center gap-1.5"><span class="text-[10px] text-slate-400 w-12">Shadow:</span><input type="text" x-model="item.shadowHover" class="cms-input-field text-xs px-2 py-1 border rounded w-full" /></div>
                            <div class="flex items-center gap-1.5"><span class="text-[10px] text-slate-400 w-12">Border:</span><input type="text" x-model="item.borderHover" class="cms-input-field text-xs px-2 py-1 border rounded w-full" /></div>
                        </div>
                    </div>
                </template>
                <div x-show="items.length === 0">
                    <p class="text-[11px] text-slate-400 italic py-2">No journey steps added yet.</p>
                </div>
            </div>
            
            <div class="cms-form-box space-y-3 p-4 border rounded-xl shadow-sm">
                <h4 class="text-[11px] font-bold text-slate-700 uppercase tracking-wide border-b border-slate-50 pb-1">Add New Step</h4>
                <div class="grid sm:grid-cols-3 gap-2">
                    <input type="text" x-model="newNum" placeholder="Num (e.g. 01)" class="cms-input-field text-xs px-3 py-2 border rounded-lg" />
                    <input type="text" x-model="newTitle" placeholder="Title" class="cms-input-field text-xs px-3 py-2 border rounded-lg col-span-2" />
                </div>
                <textarea x-model="newDesc" rows="2" placeholder="Description..." class="cms-input-field w-full text-xs px-3 py-2 border rounded-lg"></textarea>
                <div class="grid sm:grid-cols-2 gap-2">
                    <input type="text" x-model="newIcon" placeholder="Icon (e.g. ClipboardList)" class="cms-input-field text-xs px-3 py-2 border rounded-lg" />
                    <input type="text" x-model="newColor" placeholder="Color (e.g. text-blue-500)" class="cms-input-field text-xs px-3 py-2 border rounded-lg" />
                </div>
                <button type="button" @click="addItem()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold text-[10px] rounded-lg border-0 cursor-pointer uppercase tracking-wider">
                    Add Step
                </button>
            </div>
        </div>
        '''
        return mark_safe(html)

