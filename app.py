# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)


# 加载数据函数
def load_data(file_name):
    try:
        with open(f'data/{file_name}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载{file_name}数据失败: {e}")
        return {}


# 保存数据函数
def save_data(file_name, data):
    try:
        with open(f'data/{file_name}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存{file_name}数据失败: {e}")
        return False


# 主页路由
@app.route('/')
def index():
    homepage_data = load_data('homepage')
    return render_template('index.html',
                           homepage=homepage_data,
                           study=load_data('study'),
                           life=load_data('campus_life'),
                           activities=load_data('activities'),
                           practical=load_data('practical_info'),
                           community=load_data('community'))


# 添加信息的路由
@app.route('/add_info', methods=['POST'])
def add_info():
    category = request.form.get('category')
    field = request.form.get('field')
    data = request.form.get('data')

    if not all([category, field, data]):
        return jsonify({'success': False, 'message': '缺少必要参数'})

    # 加载现有数据
    existing_data = load_data(category)

    try:
        new_data = json.loads(data)

        # 如果是数组字段，添加到数组
        if field in existing_data and isinstance(existing_data[field], list):
            existing_data[field].append(new_data)
        else:
            existing_data[field] = new_data

        # 保存数据
        if save_data(category, existing_data):
            return jsonify({'success': True, 'message': '信息添加成功'})
        else:
            return jsonify({'success': False, 'message': '保存失败'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'数据格式错误: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

