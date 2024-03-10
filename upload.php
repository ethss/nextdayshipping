<?php
// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if file was uploaded without errors
    if (isset($_FILES["mp4file"]) && $_FILES["mp4file"]["error"] == 0) {
        $allowed_types = array('video/mp4');
        $file_info = finfo_open(FILEINFO_MIME_TYPE);
        $mime_type = finfo_file($file_info, $_FILES["mp4file"]["tmp_name"]);
        finfo_close($file_info);
        
        // Check if the uploaded file is of allowed type
        if (in_array($mime_type, $allowed_types)) {
            // Set destination path to save the uploaded file
            $upload_dir = "uploads/";
            $upload_file = $upload_dir . basename($_FILES["mp4file"]["name"]);
            
            // Move the uploaded file to the destination directory
            if (move_uploaded_file($_FILES["mp4file"]["tmp_name"], $upload_file)) {
                // Display the URL of the uploaded file
                $file_url = 'http://' . $_SERVER['HTTP_HOST'] . '/' . $upload_file;
                echo "File uploaded successfully. You can access it <a href=\"$file_url\">here</a>.";
            } else {
                echo "Sorry, there was an error uploading your file.";
            }
        } else {
            echo "Sorry, only MP4 files are allowed.";
        }
    } else {
        echo "Error: No file uploaded or an error occurred during upload.";
    }
} else {
    echo "Error: Invalid request method.";
}
?>
