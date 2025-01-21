import {useEffect, useState} from "react";
import {listBooks} from "../../../utils/api.ts";

export default function ListBooks() {

    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {

        setLoading(true);

        listBooks()
            .then(response => setBooks(response.data.books))
            .finally(() => setLoading(false))

    }, [])

    return (<>
        <h3>Your Books</h3>
        {loading && <article aria-busy="true"/>}
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
            </tr>
            </thead>
            <tbody>
                {books.map(book => (
                    <tr key={book.book_id}>
                        <td>{book?.book_id}</td>
                        <td>{book?.title}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </>);
}