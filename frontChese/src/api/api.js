import axiosInstance from './index'

const axios = axiosInstance

export const makesize = () => { return axios.get(`http://localhost:8000/api/make_size?size=15/`)}

//export const postBook = (bookName, bookAuthor) => {return axios.post(`http://localhost:8000/api/books/`, {'name': bookName, 'author': bookAuthor})}
