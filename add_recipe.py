#!/usr/bin/env python3
import sys
import json
import datetime
import subprocess
import os

VALID_CATEGORIES = {"refeicao", "lanche", "sobremesa"}

def normalize_category(cat):
    if not cat:
        return "refeicao"
    c = str(cat).lower().strip()
    if c in {"refeicao", "refeição", "almoco", "almoço", "jantar", "prato principal"}:
        return "refeicao"
    if c in {"lanche", "lanches", "cafe", "café", "pao", "pão"}:
        return "lanche"
    if c in {"sobremesa", "sobremesas", "doce", "doces", "bolo", "bolos"}:
        return "sobremesa"
    return "refeicao"

def add_recipe(recipe_data):
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(repo_dir, "receitas.json")
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                recipes = json.load(f)
            except Exception:
                recipes = []
    else:
        recipes = []
        
    now = datetime.datetime.now()
    recipe_id = recipe_data.get("id") or f"rec_{int(now.timestamp())}"
    title = recipe_data.get("title", "Sem Título").strip()
    category = normalize_category(recipe_data.get("category"))
    prep_time = recipe_data.get("prepTime", "N/A").strip()
    servings = recipe_data.get("servings", "N/A").strip()
    source_url = recipe_data.get("sourceUrl", "").strip()
    ingredients = recipe_data.get("ingredients") or []
    instructions = recipe_data.get("instructions") or []
    is_cooked = bool(recipe_data.get("isCooked", False))
    rating = int(recipe_data.get("rating", 0))
    if rating < 0 or rating > 5:
        rating = 0
    my_notes = recipe_data.get("myNotes", "").strip()
    created_at = recipe_data.get("createdAt") or now.strftime("%Y-%m-%d")
    
    new_entry = {
        "id": recipe_id,
        "title": title,
        "category": category,
        "prepTime": prep_time,
        "servings": servings,
        "sourceUrl": source_url,
        "ingredients": [str(i).strip() for i in ingredients if str(i).strip()],
        "instructions": [str(step).strip() for step in instructions if str(step).strip()],
        "isCooked": is_cooked,
        "rating": rating,
        "myNotes": my_notes,
        "createdAt": created_at
    }
    
    recipes.insert(0, new_entry)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
        
    print(f"✓ Receita '{title}' adicionada com sucesso ({category})!")
    
    # Git sync if git repo
    git_dir = os.path.join(repo_dir, ".git")
    if os.path.exists(git_dir):
        subprocess.run(["git", "add", "receitas.json"], cwd=repo_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"feat(receita): adiciona {title}"], cwd=repo_dir, capture_output=True)
        res = subprocess.run(["git", "push"], cwd=repo_dir, capture_output=True, text=True)
        if res.returncode == 0:
            print("✓ Sincronizado com repositório remoto via git push.")

    return new_entry

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 add_recipe.py '<JSON>' ou python3 add_recipe.py --file <caminho.json>")
        sys.exit(1)
        
    arg1 = sys.argv[1]
    if arg1 == "--file" and len(sys.argv) >= 3:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif os.path.isfile(arg1):
        with open(arg1, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Tenta interpretar como JSON string
        try:
            data = json.loads(arg1)
        except Exception as e:
            print(f"Erro ao parsear JSON: {e}")
            sys.exit(1)
            
    add_recipe(data)
