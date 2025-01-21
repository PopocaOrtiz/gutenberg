import * as api from '../../../utils/api'
import {useState} from "react";
import Error from "../../UI/Error.tsx";
import BookModal from "../BookModal/BookModal.tsx";

export default function GetBook() {

    const [bookId, setBookId] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const [bookData, setBookData] = useState<any | null>();

    const getBookHandler = async (e) => {
        e.preventDefault();

        try {
            setLoading(true);
            const response = await api.getBook(bookId);
            setLoading(false);

            if (response.error) {
                setError(response.error);
                return;
            }

            setBookData(response?.data?.book);

        } catch (e) {
            setLoading(false);
            setError('unexpected error');
            throw e;
        }
    }

    return (<div>
        <h3>Get Book</h3>
        <form>
            <fieldset role="group">
                <input
                    onChange={(e) => setBookId(e.target.value)}
                    value={bookId}
                    type="text"
                    placeholder="Enter book id to get"/>
                <input
                    onClick={(e) => getBookHandler(e)}
                    type="submit"
                    value="Get book"/>
            </fieldset>
        </form>
        {error && <Error>{error}</Error>}
        {loading && <article aria-busy="true"/>}
        {bookData && <BookModal onClose={() => setBookData(null)} bookData={bookData}/>}
    </div>);
}