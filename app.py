from flask import Flask, request, render_template, redirect, url_for
from models import Note, session
from flask_paginate import Pagination, get_page_parameter
import markdown2

app = Flask(__name__)


@app.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 7
    notes = session.query(Note).all()
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(page=page, per_page=per_page, total=len(notes))
    notes = notes[start:end]
    return render_template('notes.html', notes=notes, pagination=pagination)


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def note_detail(note_id):
    note = session.query(Note).get(note_id)
    markdown_content = markdown2.markdown(note.content)
    return render_template(
        'note.html',
        markdown_content=markdown_content,
        note=note
        )


@app.route('/search')
def search():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    query = request.args.get('query')
    notes = session.query(Note).filter(
        Note.title.ilike(f'%{query}%') | (Note.content.ilike(f'%{query}%'))
        ).all()
    per_page = 3
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=len(notes),
        )
    notes = notes[start:end]
    return render_template(
        'search_results.html',
        notes=notes,
        pagination=pagination
        )


@app.route('/add', methods=['POST'])
def add_note():
    if request.method == 'POST':
        session.add(
            Note(
                title=request.form.get('title'),
                content=request.form.get('content'),
                )
            )
        session.commit()
        return redirect(url_for('index'))


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = session.query(Note).get(note_id)
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        session.commit()
        return redirect(url_for('note_detail', note_id=note_id))
    return render_template('edit_note.html', note=note)


if __name__ == '__main__':
    app.run(debug=True)
