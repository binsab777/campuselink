<?php
namespace App\Services;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

class FileStorageService {
    public function upload(UploadedFile $file, string $directory, string $filename = null) {
        if (!$file->isValid()) throw new \Exception("Invalid file upload");
        $name = $filename ?? $file->hashName();
        $path = $file->storeAs($directory, $name, 'local');
        return url('/api/v1/files/' . $path);
    }
    public function delete(string $url) {
        $path = str_replace('/api/v1/files/', '', parse_url($url, PHP_URL_PATH));
        if (Storage::disk('local')->exists($path)) {
            Storage::disk('local')->delete($path);
        }
    }
}
