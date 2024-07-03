const mongoose = require('mongoose');

const { Schema } = mongoose;

const carSchema = new Schema({
    dealerId: {
        type: Number,
        required: true
    },
    make: {
        type: String,
        required: true
    },
    model: {
        type: String,
        required: true
    },
    bodyType: {
        type: String,
        required: true
    },
    year: {
        type: Number,
        required: true
    },
    mileage: {
        type: Number,
        required: true
    }
});

// Export the model
module.exports = mongoose.model('Car', carSchema);
