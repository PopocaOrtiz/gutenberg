import GetBook from "./GetBook/GetBook.tsx";
import ListBooks from "./ListBooks/ListBooks.tsx";
import Title from "../UI/Title.tsx";

export default function Books() {
    return (<>
        <Title title="Books" description=""/>
        <GetBook/>
        <ListBooks/>
    </>);
}
