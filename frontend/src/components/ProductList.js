import React, { useState, useEffect } from "react";
import axios from "axios";
import API_URL from "../apiConfig";
import { socket, joinRoom } from "../socket";

function ProductList() {
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({ sku: "", name: "", active: "" });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [deleteStatus, setDeleteStatus] = useState("");
  const [deleteError, setDeleteError] = useState("");

  const fetchProducts = async () => {
    try {
      const params = {
        page,
        sku: filters.sku,
        name: filters.name,
        active: filters.active,
      };
      const res = await axios.get(`${API_URL}/api/products`, { params });
      setProducts(res.data.products);
      setTotalPages(res.data.total_pages);
    } catch (err) {
      console.error("Error fetching products:", err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [filters, page]);

  useEffect(() => {
    socket.on("task_complete", (data) => {
      setDeleteStatus(data.status);
      setDeleteError("");
      fetchProducts();
    });
    socket.on("task_failed", (data) => {
      setDeleteError(data.error);
      setDeleteStatus("");
    });
    return () => {
      socket.off("task_complete");
      socket.off("task_failed");
    };
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
    setPage(1);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      try {
        await axios.delete(`${API_URL}/api/products/${id}`);
        fetchProducts();
      } catch (err) {
        console.error("Error deleting product:", err);
      }
    }
  };

  const handleBulkDelete = async () => {
    if (window.confirm("Are you sure? This cannot be undone.")) {
      try {
        setDeleteStatus("Deletion in progress...");
        setDeleteError("");
        const res = await axios.delete(`${API_URL}/api/products/delete-all`);
        joinRoom(res.data.job_id);
      } catch (err) {
        setDeleteError("Failed to start bulk delete.");
        setDeleteStatus("");
      }
    }
  };

  return (
    <div className="card">
      <h3>Story 2 & 3: Product Management</h3>

      <div className="bulk-delete">
        <button onClick={handleBulkDelete} className="danger-button">
          Delete All Products
        </button>
        {deleteStatus && <p className="success">{deleteStatus}</p>}
        {deleteError && <p className="error">{deleteError}</p>}
      </div>

      <div className="filters">
        <input
          name="sku"
          value={filters.sku}
          onChange={handleFilterChange}
          placeholder="Filter by SKU..."
        />
        <input
          name="name"
          value={filters.name}
          onChange={handleFilterChange}
          placeholder="Filter by Name..."
        />
        <select
          name="active"
          value={filters.active}
          onChange={handleFilterChange}
        >
          <option value="">All Status</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
      </div>

      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Description</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.sku}</td>
              <td>{p.name}</td>
              <td>
                {p.description ? p.description.substring(0, 50) + "..." : ""}
              </td>
              <td>{p.active ? "Active" : "Inactive"}</td>
              <td>
                <button
                  onClick={() => handleDelete(p.id)}
                  className="small-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
          disabled={page === 1}
        >
          &laquo; Prev
        </button>
        <span>
          Page {page} of {totalPages}
        </span>
        <button
          onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
          disabled={page === totalPages}
        >
          Next &raquo;
        </button>
      </div>
    </div>
  );
}

export default ProductList;
