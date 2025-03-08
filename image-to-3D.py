import cv2
import numpy as np
import open3d as o3d

def extract_views(image_path):
    """Extracts the required six views from the image."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    h_step, w_step = h // 3, w // 4
    
    views = {
        'top': img[0:h_step, w_step:2*w_step],
        'right': img[h_step:2*h_step, 0:w_step],
        'front': img[h_step:2*h_step, w_step:2*w_step],
        'left': img[h_step:2*h_step, 2*w_step:3*w_step],
        'rear': img[h_step:2*h_step, 3*w_step:4*w_step],
        'bottom': img[2*h_step:3*h_step, w_step:2*w_step]
    }
    return views

def silhouette_to_points(view, axis, position):
    """Convert a silhouette to 3D points."""
    points = []
    h, w = view.shape
    
    for y in range(h):
        for x in range(w):
            if view[y, x] < 128:  # Threshold for silhouette (black pixels)
                if axis == 'xy':
                    points.append([x, h - y, position])
                elif axis == 'xz':
                    points.append([x, position, h - y])
                elif axis == 'yz':
                    points.append([position, x, h - y])
    return points

def generate_3d_model(views):
    """Creates a 3D point cloud from multiple silhouettes."""
    point_cloud = []
    
    point_cloud += silhouette_to_points(views['top'], 'xy', 10)
    point_cloud += silhouette_to_points(views['bottom'], 'xy', -10)
    point_cloud += silhouette_to_points(views['front'], 'xz', 10)
    point_cloud += silhouette_to_points(views['rear'], 'xz', -10)
    point_cloud += silhouette_to_points(views['left'], 'yz', -10)
    point_cloud += silhouette_to_points(views['right'], 'yz', 10)
    
    return np.array(point_cloud)

def create_mesh_from_points(points):
    """Converts point cloud to a 3D mesh."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd)
    return mesh

def save_mesh(mesh, filename="output.obj"):
    """Saves the mesh as an OBJ file."""
    o3d.io.write_triangle_mesh(filename, mesh)
    print(f"Mesh saved as {filename}")

if __name__ == "__main__":
    image_path = "test-views.jpg"  # Change this to your image file
    views = extract_views(image_path)
    points = generate_3d_model(views)
    mesh = create_mesh_from_points(points)
    save_mesh(mesh)
    o3d.visualization.draw_geometries([mesh])
