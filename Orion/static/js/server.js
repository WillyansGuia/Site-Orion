require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

app.listen(5000, () => console.log("Server running on port 5500"));

const authRoutes = require("/routes/auth");

app.use("/auth", authRoutes);
