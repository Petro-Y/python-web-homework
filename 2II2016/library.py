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


if __name__=='__main__':
    init_db()
    add_book('The Book of the Books', ['God', 'Jesus Christ', 'Flying Spaghetti Monster'])
    list_books()

