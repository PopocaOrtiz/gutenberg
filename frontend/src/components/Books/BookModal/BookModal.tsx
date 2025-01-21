import Modal from "../../UI/Modal";

export default function BookModal({ onClose, bookData}) {
    return (<Modal onClose={() => onClose()} title={bookData.title}>
        {bookData.author}
    </Modal>);
}