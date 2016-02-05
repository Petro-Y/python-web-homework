import sqlite3

def init_db():
    conn=sqlite3.connect('library')
    cur=conn.cursor()
    cur.executescript('''
    drop table if exists Book;
    drop table if exists Author;
    drop table if exists BookAuthor;
    create table Book (id integer primary key autoincrement, title text);
    create table Author (id integer primary key autoincrement, name text);
    create table BookAuthor (book_id integer, author_id integer);
    insert into Book values (0, 'Reading for Dummies'), (1, 'Assembler for Web developers');
    insert into Author values (0, 'John Johnson'), (1, 'Anonimous Nameless'), (2, 'Unknown Author');
    insert into BookAuthor values (0, 0), (1, 1), (1, 2)
    ''')
    conn.commit()
    cur.close()
    conn.close()

def list_books():
    conn=sqlite3.connect('library')
    cur=conn.cursor()
    cur.execute('''
    select title, group_concat(name) from Book
    join BookAuthor on Book.id=BookAuthor.book_id
    join Author on Author.id=BookAuthor.author_id
    group by title
    ''')
    for row in cur:
        print(row)
    cur.close()
    conn.close()

def add_book(title, authors):
    conn=sqlite3.connect('library')
    cur=conn.cursor()
    cur.execute('''
    insert into Book (title) values(?)
    ''', [title])
    cur.execute('''
    select max(id) from Book where title=? group by title
    ''', [title])
    for row in cur:
        #print(row)
        book_id=row[0]
    for author in authors:
        #if author not in db, insert him:
        cur.execute('''
        select max(id) from Author where name=? group by name
        ''', [author])
        for row in cur:
            author_id=row[0]
        else:
            cur.execute('''
            insert into Author (name) values(?)
            ''', [author])
            cur.execute('''
            select max(id) from Author where name=? group by name
            ''', [author])
            for row in cur:
                author_id=row[0]
        cur.execute('''
        insert into BookAuthor values(?, ?)
        ''', [book_id, author_id])
    conn.commit()
    cur.close()
    conn.close()

##################
from flask import Flask, request, redirect
app = Flask(__name__)

import urllib
def split_authors(s):
    return ', '.join(map(lambda a: '<a href="/?author=%s">%s</a>' %(urllib.quote(a),a),s.split('|')))

@app.route('/', methods=['GET'])
def web_list_books():
    try:
        author=request.args.get('author')
    except Exception:
        author=None
    print('autor:', author)
    res=''
    conn=sqlite3.connect('library')
    cur=conn.cursor()
    cur.execute('''
    select title, group_concat(name, '|') from Book join BookAuthor on Book.id=BookAuthor.book_id
    join Author on Author.id=BookAuthor.author_id'''
    +(" where name='"+author+"' " if author else ' ')+
    '''
    group by book_id
    ''')
    for row in cur:
        res+='<li>%s - <b>%s</b></li>'%(split_authors(row[1]), row[0])
        #print(row)
    cur.close()
    conn.close()
    res='''
    <ul>
    %s
    </ul>

    <form action=add method=POST>
        <input name=book><br>
        <textarea name=authors></textarea><br>
        <input type=submit>
    </form>
    '''%res
    return res

@app.route('/add', methods=['POST'])
def web_add_book():
    book=request.form['book']
    authors=map(str.strip, request.form['authors'].split('\n'))
    add_book(book, authors)
    return redirect('/')


if __name__=='__main__':
    #init_db()
    #add_book('The Book of the Books', ['God', 'Jesus Christ', 'Flying Spaghetti Monster'])
    #list_books()
    app.run()

